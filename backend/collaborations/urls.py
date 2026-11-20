
from django.urls import path

from .views import (
    CandidatureAgronomeListCreateAPIView,
    CandidatureAgronomeDetailAPIView,
    CandidatureAgronomeAdminListAPIView,
    DecisionCandidatureAPIView,
    DocumentCandidatureUploadAPIView,
    DocumentCandidatureDownloadAPIView,
)

urlpatterns = [
    path(
        "candidatures/",
        CandidatureAgronomeListCreateAPIView.as_view(),
        name="candidature-list-create"
    ),
    path(
        "admin/candidatures/",
        CandidatureAgronomeAdminListAPIView.as_view(),
        name="admin-candidature-list"
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
    path(
        "candidatures/<int:candidature_id>/documents/",
        DocumentCandidatureUploadAPIView.as_view(),
        name="candidature-documents"
    ),
    path(
        "documents/<int:pk>/telecharger/",
        DocumentCandidatureDownloadAPIView.as_view(),
        name="candidature-document-download"
    ),
]
