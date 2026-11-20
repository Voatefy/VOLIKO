import logging

from django.utils import timezone

from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from notifications.models import TypeNotification

from .serializers import (
    CandidatureAgronomeSerializer,
    CandidatureAgronomeAdminSerializer,
    DecisionCandidatureSerializer,
    DocumentCandidatureUploadSerializer,
    DocumentCandidatureReadSerializer,
    AutorisationAccesSerializer,
    DecisionAutorisationSerializer,
)

from notifications.services import (
    envoyer_notification_application,
    envoyer_notification_email,
)

from .models import (
    CandidatureAgronome,
    DocumentCandidature,
    StatutCandidature,
    AutorisationAcces,
    PorteeAcces,
    StatutDemandeAcces,
    StatutAutorisation,
)

logger = logging.getLogger(__name__)

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


class CandidatureAgronomeAdminListAPIView(generics.ListAPIView):

    serializer_class = CandidatureAgronomeAdminSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        if self.request.user.role != "ADMINISTRATEUR":
            raise PermissionDenied(
                "Seul un administrateur peut consulter les candidatures."
            )

        queryset = CandidatureAgronome.objects.filter(
            date_candidature__isnull=False
        ).select_related(
            "candidat",
            "administrateur"
        )

        statut = self.request.query_params.get("statut")

        if statut:
            statuts_valides = [
                choix[0] for choix in StatutCandidature.choices
            ]

            if statut not in statuts_valides:

                raise ValidationError({
                    "statut": "Statut de candidature invalide."
                })

            queryset = queryset.filter(statut=statut)

        return queryset.order_by("-date_candidature")


class DecisionCandidatureAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        if request.user.role != "ADMINISTRATEUR":
            raise PermissionDenied(
                "Seul un administrateur peut traiter une candidature."
            )

        serializer = DecisionCandidatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ===
        nouveau_statut = serializer.validated_data["statut"]

        contenu_email = (
            "Votre candidature d'agronome a été acceptée. Félicitations !"
            if nouveau_statut == StatutCandidature.ACCEPTEE
            else (
                "Votre candidature d'agronome a été refusée.\n"
                f"Motif : {serializer.validated_data.get('motif_decision', '')}"
            )
        )
        # ===
        with transaction.atomic():

            candidature = get_object_or_404(
                CandidatureAgronome.objects.select_for_update(),
                pk=pk
            )

            # hehehe
            if candidature.statut not in [
                StatutCandidature.SOUMISE,
                StatutCandidature.EN_EXAMEN,
            ]:
                raise PermissionDenied(
                    "Cette candidature ne peut pas être traitée "
                    "dans son état actuel."
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

            envoyer_notification_application(
                destinataire=candidature.candidat,
                categorie=TypeNotification.CANDIDATURE,
                contenu=(
                    "Votre candidature d'agronome a été acceptée."
                    if nouveau_statut == StatutCandidature.ACCEPTEE
                    else (
                        "Votre candidature d'agronome a été refusée. "
                        f"Motif : {candidature.motif_decision}"
                    )
                ),
            )
        # ===
        try:
            envoyer_notification_email(
                destinataire=candidature.candidat,
                categorie=TypeNotification.CANDIDATURE,
                sujet="Décision concernant votre candidature VOLIKO",
                contenu=contenu_email,
            )
        except Exception:
            logger.exception(
                "Échec de l'envoi de l'e-mail de décision de candidature."
            )
        # ===

        return Response(
            CandidatureAgronomeSerializer(candidature).data,
            status=status.HTTP_200_OK
        )



class DocumentCandidatureUploadAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, candidature_id):

        candidature = get_object_or_404(
            CandidatureAgronome,
            pk=candidature_id
        )

        est_candidat = candidature.candidat_id == request.user.id
        est_admin = request.user.role == "ADMINISTRATEUR"

        if not est_candidat and not est_admin:
            raise PermissionDenied(
                "Vous n'êtes pas autorisé à consulter ces documents."
            )

        if est_admin and candidature.date_candidature is None:
            raise PermissionDenied(
                "Cette candidature n'a pas encore été soumise."
            )

        documents = candidature.documents.all().order_by("-date_ajout")

        return Response(
            DocumentCandidatureReadSerializer(
                documents,
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, candidature_id):

        candidature = get_object_or_404(
            CandidatureAgronome,
            pk=candidature_id,
            candidat=request.user
        )

        if candidature.statut in [
            StatutCandidature.ACCEPTEE,
            StatutCandidature.REJETEE,
        ]:
            raise PermissionDenied(
                "Cette candidature ne peut plus recevoir de documents."
            )

        serializer = DocumentCandidatureUploadSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        document = serializer.save(candidature=candidature)

        return Response(
            DocumentCandidatureUploadSerializer(document).data,
            status=status.HTTP_201_CREATED
        )


# Documents
class DocumentCandidatureListAPIView(generics.ListAPIView):

    serializer_class = DocumentCandidatureReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        candidature = get_object_or_404(
            CandidatureAgronome,
            pk=self.kwargs["candidature_id"]
        )

        if (
            candidature.candidat_id != self.request.user.id
            and self.request.user.role != "ADMINISTRATEUR"
        ):
            raise PermissionDenied(
                "Vous n'êtes pas autorisé à consulter ces documents."
            )

        if (
            self.request.user.role == "ADMINISTRATEUR"
            and candidature.date_candidature is None
        ):
            raise PermissionDenied(
                "Cette candidature n'a pas encore été soumise."
            )

        return candidature.documents.all().order_by("-date_ajout")


class DocumentCandidatureDownloadAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        document = get_object_or_404(
            DocumentCandidature.objects.select_related(
                "candidature",
                "candidature__candidat"
            ),
            pk=pk
        )

        candidature = document.candidature

        est_candidat = candidature.candidat_id == request.user.id
        est_admin = request.user.role == "ADMINISTRATEUR"

        if not est_candidat and not est_admin:
            raise PermissionDenied(
                "Vous n'êtes pas autorisé à télécharger ce document."
            )

        if est_admin and candidature.date_candidature is None:
            raise PermissionDenied(
                "Cette candidature n'a pas encore été soumise."
            )

        fichier = document.chemin_stockage

        if not fichier or not fichier.storage.exists(fichier.name):
            raise ValidationError(
                "Le fichier demandé est introuvable."
            )

        return FileResponse(
            fichier.open("rb"),
            as_attachment=True,
            filename=document.nom_fichier
        )



# ==================================================
# AUTORISATIONS D'ACCÈS AUX PARCELLES
# ==================================================

class AutorisationAccesListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = AutorisationAccesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        utilisateur = self.request.user

        if utilisateur.role == "AGRONOME":
            return AutorisationAcces.objects.filter(
                agronome=utilisateur
            ).select_related(
                "agriculteur",
                "agronome",
                "parcelle"
            ).order_by("-date_demande")

        return AutorisationAcces.objects.none()

    def perform_create(self, serializer):

        utilisateur = self.request.user

        if utilisateur.role != "AGRONOME":
            raise PermissionDenied(
                "Seul un agronome peut demander une autorisation."
            )

        agriculteur = self.request.data.get("agriculteur")
        portee = self.request.data.get("portee")
        parcelle = self.request.data.get("parcelle")

        demandes = AutorisationAcces.objects.filter(
            agronome=utilisateur,
            agriculteur_id=agriculteur,
            portee=portee,
        )

        if portee == PorteeAcces.PARCELLE:
            demandes = demandes.filter(parcelle_id=parcelle)
        else:
            demandes = demandes.filter(parcelle__isnull=True)

        demande_en_attente = demandes.filter(
            statut_demande=StatutDemandeAcces.EN_ATTENTE
        ).exists()

        autorisation_active = demandes.filter(
            statut_autorisation=StatutAutorisation.ACTIVE
        ).exists()

        if demande_en_attente or autorisation_active:
            raise ValidationError(
                "Une demande en attente ou une autorisation active existe déjà."
            )

        serializer.save(
            agronome=utilisateur,
            statut_demande=StatutDemandeAcces.EN_ATTENTE,
            statut_autorisation=StatutAutorisation.INACTIVE
        )


class AutorisationsRecuesAPIView(generics.ListAPIView):

    serializer_class = AutorisationAccesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        utilisateur = self.request.user

        if utilisateur.role != "AGRICULTEUR":
            raise PermissionDenied(
                "Seul un agriculteur peut consulter les demandes reçues."
            )

        return AutorisationAcces.objects.filter(
            agriculteur=utilisateur
        ).select_related(
            "agriculteur",
            "agronome",
            "parcelle"
        ).order_by("-date_demande")




class DecisionAutorisationAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        if request.user.role != "AGRICULTEUR":
            raise PermissionDenied(
                "Seul un agriculteur peut décider d'une demande."
            )

        serializer = DecisionAutorisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():

            autorisation = get_object_or_404(
                AutorisationAcces.objects.select_for_update(),
                pk=pk,
                agriculteur=request.user
            )

            if autorisation.statut_demande != StatutDemandeAcces.EN_ATTENTE:
                raise ValidationError(
                    "Cette demande a déjà été traitée."
                )

            maintenant = timezone.now()

            autorisation.statut_demande = serializer.validated_data["statut"]
            autorisation.date_decision = maintenant

            if autorisation.statut_demande == StatutDemandeAcces.ACCEPTEE:

                autorisation.statut_autorisation = StatutAutorisation.ACTIVE
                autorisation.date_autorisation = maintenant

            else:

                autorisation.statut_autorisation = StatutAutorisation.INACTIVE
                autorisation.date_autorisation = None

            autorisation.save(update_fields=[
                "statut_demande",
                "date_decision",
                "statut_autorisation",
                "date_autorisation",
            ])

        return Response(
            AutorisationAccesSerializer(autorisation).data,
            status=status.HTTP_200_OK
        )



class RevoquerAutorisationAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        if request.user.role != "AGRICULTEUR":
            raise PermissionDenied(
                "Seul un agriculteur peut révoquer une autorisation."
            )

        with transaction.atomic():

            autorisation = get_object_or_404(
                AutorisationAcces.objects.select_for_update(),
                pk=pk,
                agriculteur=request.user
            )

            if autorisation.statut_autorisation != StatutAutorisation.ACTIVE:
                raise ValidationError(
                    "Seule une autorisation active peut être révoquée."
                )

            autorisation.statut_autorisation = StatutAutorisation.REVOQUEE
            autorisation.date_revocation = timezone.now()

            autorisation.save(update_fields=[
                "statut_autorisation",
                "date_revocation",
            ])

        return Response(
            AutorisationAccesSerializer(autorisation).data,
            status=status.HTTP_200_OK
        )