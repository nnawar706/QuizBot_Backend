from django.urls import path
from .views import *

urlpatterns = [
    path("register", UserRegistrationView.as_view()),
    path('me', RetrieveUsersView.as_view())
]