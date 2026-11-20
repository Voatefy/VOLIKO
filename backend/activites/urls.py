
from django.urls import path

from .views import (
    ActivitePlanifieeListCreateAPIView,
    ActivitePlanifieeDetailAPIView,
    ActiviteAgricoleListCreateAPIView,
    ActiviteAgricoleDetailAPIView,
)

urlpatterns = [
    path(
        "",
        ActivitePlanifieeListCreateAPIView.as_view(),
        name="activites-planifiees",
    ),
    path(
        "<int:pk>/",
        ActivitePlanifieeDetailAPIView.as_view(),
        name="activite-planifiee-detail",
    ),
    path(
        "realisees/",
        ActiviteAgricoleListCreateAPIView.as_view(),
        name="activites-realisees",
    ),
    path(
        "realisees/<int:pk>/",
        ActiviteAgricoleDetailAPIView.as_view(),
        name="activite-realisee-detail",
    ),
]
