
from django.urls import path

from .views import (
    NotificationListAPIView,
    NotificationDetailAPIView,
    NotificationMarquerLueAPIView,
    PreferenceNotificationListCreateAPIView,
    PreferenceNotificationDetailAPIView,
)

urlpatterns = [
    path(
        "",
        NotificationListAPIView.as_view(),
        name="notification-list"
    ),
    path(
        "preferences/",
        PreferenceNotificationListCreateAPIView.as_view(),
        name="preference-notification-list-create"
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

    path(
        "preferences/<int:pk>/",
        PreferenceNotificationDetailAPIView.as_view(),
        name="preference-notification-detail",
    ),
]
