from django.urls import path

from .views import (
    NotificationListAPIView,
    NotificationDetailAPIView,
    NotificationMarquerLueAPIView,
)

urlpatterns = [
    path(
        "",
        NotificationListAPIView.as_view(),
        name="notification-list"
    ),
    path(
        "<int:pk>/",
        NotificationDetailAPIView.as_view(),
        name="notification-detail"
    ),
    path(
        "<int:pk>/lue/",
        NotificationMarquerLueAPIView.as_view(),
        name="notification-marquer-lue"
    ),
]
