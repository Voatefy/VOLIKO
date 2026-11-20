
from django.urls import path

from .views import (
    ParcelleListCreateAPIView,
    ParcelleDetailAPIView,
    CultureParcelleListCreateAPIView,
    CultureParcelleDetailAPIView,
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
    path(
        "cultures/",
        CultureParcelleListCreateAPIView.as_view(),
        name="culture-parcelle-list-create"
    ),
    path(
        "cultures/<int:pk>/",
        CultureParcelleDetailAPIView.as_view(),
        name="culture-parcelle-detail"
    ),
]
