import base64
import logging
from functools import partial

from django.conf import settings
from googleapiclient.discovery import Resource
from googleapiclient.http import BatchHttpRequest

from app.google_services import get_storage_client, get_datastore_client
from core.models import EmailMessage
from core.utils import get_sender

logger = logging.getLogger(__name__)


def handle_messages_details(
    message_list: dict, gmail_client: Resource, user_email: str
) -> None:
    batch = BatchHttpRequest()

    for i in message_list["messages"]:
        callback = partial(
            find_and_save_flight_bookings, service=gmail_client, user_id=user_email
        )
        batch.add(
            gmail_client.users().messages().get(userId=user_email, id=i["id"]),
            callback=callback,
        )

    batch.execute()


def find_and_save_flight_bookings(
    request: str, message: dict, exception: Exception, service: Resource, user_id: str
) -> None:
    storage = get_storage_client()
    datastore = get_datastore_client()
    bucket = storage.bucket(settings.BUCKET_NAME)

    parts = [message["payload"]]
    files = list()

    while parts:
        try:
            part = parts.pop()

            if part.get("parts"):
                parts.extend(part["parts"])

            if part.get("filename") and "pdf" in part["filename"]:
                if "attachmentId" in part["body"]:
                    attachment = (
                        service.users()
                        .messages()
                        .attachments()
                        .get(
                            userId=user_id,
                            messageId=message["id"],
                            id=part["body"]["attachmentId"],
                        )
                        .execute()
                    )
                    file_data = base64.urlsafe_b64decode(
                        attachment["data"].encode("UTF-8")
                    )

                    blob = bucket.blob(f"{user_id}/{part['filename']}")
                    blob.upload_from_string(file_data, content_type="application/pdf")
                    files.append(blob.public_url)

        except Exception as e:
            logger.error(f"Can't upload file from email#{user_id} box: {e}")

    if files:
        sender = get_sender(message)
        with datastore.context():
            EmailMessage.make_record(sender, message["id"], files)
