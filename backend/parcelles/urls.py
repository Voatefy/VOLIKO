from django.urls import path

from .views import (
    ParcelleListCreateAPIView,
    ParcelleDetailAPIView,
)

urlpatterns = [
    path(
        "",
        ParcelleListCreateAPIView.as_view(),
        name="parcelle-list-create"
    ),
    path(
        "<int:pk>/",
        ParcelleDetailAPIView.as_view(),
        name="parcelle-detail"
    ),
]
