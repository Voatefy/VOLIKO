from django.utils import timezone

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    CandidatureAgronomeSerializer,
    DecisionCandidatureSerializer,
)

from notifications.models import Notification, TypeNotification

from .models import (
    CandidatureAgronome,
    StatutCandidature,
)


class CandidatureAgronomeListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = CandidatureAgronomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CandidatureAgronome.objects.filter(
            candidat=self.request.user
        )

    def perform_create(self, serializer):
        if CandidatureAgronome.objects.filter(
            candidat=self.request.user,
            statut__in=[
                StatutCandidature.BROUILLON,
                StatutCandidature.SOUMISE,
                StatutCandidature.EN_EXAMEN,
                StatutCandidature.A_CORRIGER,
            ]
        ).exists():
            raise PermissionDenied(
                "Vous avez déjà une candidature non terminée."
            )

        serializer.save(
            candidat=self.request.user,
            statut=StatutCandidature.SOUMISE,
            date_candidature=timezone.now(),
        )


class CandidatureAgronomeDetailAPIView(generics.RetrieveUpdateAPIView):

    serializer_class = CandidatureAgronomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CandidatureAgronome.objects.filter(
            candidat=self.request.user
        )

class DecisionCandidatureAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        if request.user.role != "ADMINISTRATEUR":
            raise PermissionDenied(
                "Seul un administrateur peut traiter une candidature."
            )

        serializer = DecisionCandidatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():

            candidature = get_object_or_404(
                CandidatureAgronome.objects.select_for_update(),
                pk=pk
            )

            if candidature.statut in [
                StatutCandidature.ACCEPTEE,
                StatutCandidature.REJETEE,
            ]:
                raise PermissionDenied(
                    "Cette candidature a déjà été traitée."
                )

            nouveau_statut = serializer.validated_data["statut"]

            candidature.statut = nouveau_statut
            candidature.administrateur = request.user
            candidature.motif_decision = serializer.validated_data.get(
                "motif_decision", ""
            )
            candidature.date_decision = timezone.now()

            candidature.save()

            if nouveau_statut == StatutCandidature.ACCEPTEE:
                candidature.candidat.role = "AGRONOME"
                candidature.candidat.save(update_fields=["role"])

            Notification.objects.create(
                destinataire=candidature.candidat,
                type_notification=TypeNotification.CANDIDATURE,
                contenu=(
                    "Votre candidature d'agronome a été acceptée."
                    if nouveau_statut == StatutCandidature.ACCEPTEE
                    else (
                        "Votre candidature d'agronome a été refusée. "
                        f"Motif : {candidature.motif_decision}"
                    )
                )
            )

        return Response(
            CandidatureAgronomeSerializer(candidature).data,
            status=status.HTTP_200_OK
        )