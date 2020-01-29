from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from rest_framework import generics
from rest_framework.request import Request

from app.google_services import get_oauth2_client, get_oauth_flow
from core.utils import credentials_to_dict
from core.tasks import explore_user_box


class GoogleOAuth2View(generics.GenericAPIView):
    def get(self, *args, **kwargs):
        flow = get_oauth_flow()

        authorization_url, state = flow.authorization_url(access_type="offline")
        return HttpResponseRedirect(authorization_url)


class GoogleOAuth2CallbackView(View):
    def get(self, request: Request, *args, **kwargs):
        flow = get_oauth_flow()

        flow.fetch_token(code=request.GET["code"])
        credentials = credentials_to_dict(flow.credentials)

        me = get_oauth2_client(credentials)
        user_data = me.userinfo().v2().me().get().execute()
        email = user_data["email"]

        explore_user_box(credentials, email)
        return HttpResponse(f"Hello, {email}!")
