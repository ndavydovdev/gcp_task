from django.urls import path
from .views import GoogleOAuth2CallbackView, GoogleOAuth2View

urlpatterns = [
    path("login", GoogleOAuth2View.as_view(), name="oauth2"),
    path("callback", GoogleOAuth2CallbackView.as_view(), name="callback"),
]
