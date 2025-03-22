from django.urls import path
from .views import home, upload_document, user_login, user_register

urlpatterns = [
    path("", home, name="home"),
    path("upload/", upload_document, name="upload"),
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
]
