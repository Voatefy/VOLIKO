from django.urls import path

from .views import (
    InscriptionAPIView,
    ProfilUtilisateurAPIView,
)

urlpatterns = [
    path(
        "inscription/",
        InscriptionAPIView.as_view(),
        name="inscription"
    ),
    path(
        "profil/",
        ProfilUtilisateurAPIView.as_view(),
        name="profil"
    ),
]
