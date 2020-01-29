from google_auth_oauthlib.flow import Flow
from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from google.cloud import storage, ndb


def get_oauth_flow() -> Flow:
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_CREDENTIALS,
        [
            "openid",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/userinfo.email",
        ],
    )
    flow.redirect_uri = "http://localhost:8000/callback"
    return flow


def get_gmail_client(credentials: dict) -> Resource:
    return build(
        "gmail", "v1", credentials=Credentials.from_authorized_user_info(credentials)
    )


def get_oauth2_client(credentials: dict) -> Resource:
    return build(
        "oauth2", "v2", credentials=Credentials.from_authorized_user_info(credentials)
    )


def get_storage_client() -> storage.Client:
    return storage.Client()


def get_datastore_client() -> ndb.Client:
    return ndb.Client()
