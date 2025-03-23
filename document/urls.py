from django.urls import path
from .views import home, upload_document, user_login, user_register
from django.contrib.auth import views as auth_views 
from .views import case_list, add_case, get_cases
urlpatterns = [
    path("home/", home, name="home"),  # Home page route
    path("upload/", upload_document, name="upload"),
    path("login/", user_login, name="login"),  # Login page route
    path("register/", user_register, name="register"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

]
