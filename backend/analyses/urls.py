
from django.urls import path

from .views import (
    ObservationNDVIListAPIView,
    ObservationNDVIDetailAPIView,
    DonneeMeteoListAPIView,
    DonneeMeteoDetailAPIView,
    AlerteAgricoleListAPIView,
    AlerteAgricoleDetailAPIView,
    ConseilAgricoleListAPIView,
    ConseilAgricoleDetailAPIView,
)

urlpatterns = [
    path(
        "ndvi/",
        ObservationNDVIListAPIView.as_view(),
        name="observation-ndvi-list",
    ),
    path(
        "ndvi/<int:pk>/",
        ObservationNDVIDetailAPIView.as_view(),
        name="observation-ndvi-detail",
    ),
    path(
        "meteo/",
        DonneeMeteoListAPIView.as_view(),
        name="donnee-meteo-list",
    ),
    path(
        "meteo/<int:pk>/",
        DonneeMeteoDetailAPIView.as_view(),
        name="donnee-meteo-detail",
    ),
    path(
        "alertes/",
        AlerteAgricoleListAPIView.as_view(),
        name="alerte-list",
    ),
    path(
        "alertes/<int:pk>/",
        AlerteAgricoleDetailAPIView.as_view(),
        name="alerte-detail",
    ),
    path(
        "conseils/",
        ConseilAgricoleListAPIView.as_view(),
        name="conseil-list",
    ),
    path(
        "conseils/<int:pk>/",
        ConseilAgricoleDetailAPIView.as_view(),
        name="conseil-detail",
    ),
]
