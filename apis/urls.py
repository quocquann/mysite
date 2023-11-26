from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import BookDetail, BookList, BookInstanceDetail


urlpatterns = [
    path("auth/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("books", BookList.as_view()),
    path("books/create", BookDetail.as_view()),
    path("books/<int:pk>/update", BookDetail.as_view()),
    path("books/<uuid:pk>/renew", BookInstanceDetail.as_view()),
]
