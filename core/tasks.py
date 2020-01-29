from celery import shared_task

from app.google_services import get_gmail_client
from core.internal import handle_messages_details


@shared_task
def explore_user_box(credentials: dict, user_email: str) -> None:
    gmail_client = get_gmail_client(credentials)

    message_list_response = (
        gmail_client.users()
        .messages()
        .list(userId=user_email, maxResults=100)
        .execute()
    )
    page_token = message_list_response.get("nextPageToken")

    handle_messages_details(message_list_response, gmail_client, user_email)
    while "nextPageToken" in message_list_response:
        message_list_response = (
            gmail_client.users()
            .messages()
            .list(userId=user_email, pageToken=page_token, maxResults=100)
            .execute()
        )
        page_token = message_list_response.get("nextPageToken")
        handle_messages_details(message_list_response, gmail_client, user_email)
