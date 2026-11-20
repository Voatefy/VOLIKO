from django.urls import path

from .views import (
    CandidatureAgronomeListCreateAPIView,
    CandidatureAgronomeDetailAPIView,
    DecisionCandidatureAPIView,
)

urlpatterns = [
    path(
        "candidatures/",
        CandidatureAgronomeListCreateAPIView.as_view(),
        name="candidature-list-create"
    ),
    path(
        "candidatures/<int:pk>/",
        CandidatureAgronomeDetailAPIView.as_view(),
        name="candidature-detail"
    ),
    path(
        "candidatures/<int:pk>/decision/",
        DecisionCandidatureAPIView.as_view(),
        name="candidature-decision"
    ),
]
