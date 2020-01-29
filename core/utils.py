from google.oauth2.credentials import Credentials


def credentials_to_dict(credentials: Credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def get_sender(message: dict):
    for header in message["payload"]["headers"]:
        if header.get("name") == "From":
            return header["value"]
