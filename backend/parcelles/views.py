from django.db.models import Q
from django.utils import timezone
from django.db import transaction

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Parcelle
from .serializers import ParcelleSerializer
from collaborations.models import (
    AutorisationAcces,
    PorteeAcces,
    StatutAutorisation,
)


class ParcellePermission(permissions.BasePermission):
    """
    Contrôle les droits d'accès aux parcelles.
    """

    def has_object_permission(self, request, view, obj):

        utilisateur = request.user

        # Le propriétaire peut gérer sa parcelle.
        if obj.proprietaire_id == utilisateur.id:
            return True

        # Un agronome autorisé dispose uniquement d'un accès en lecture.
        if (
            utilisateur.role != "AGRONOME"
            or request.method not in permissions.SAFE_METHODS
        ):
            return False

        return AutorisationAcces.objects.filter(
            agriculteur=obj.proprietaire,
            agronome=utilisateur,
            statut_demande="ACCEPTEE",
            statut_autorisation=StatutAutorisation.ACTIVE,
        ).filter(
            Q(
                portee=PorteeAcces.PARCELLE,
                parcelle=obj
            )
            |
            Q(
                portee=PorteeAcces.TOUTES,
                parcelle__isnull=True
            )
        ).exists()


class ParcelleListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ParcelleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        utilisateur = self.request.user

        # Les parcelles supprimées sont exclues.
        parcelles = Parcelle.objects.filter(
            date_suppression__isnull=True
        )

        # L'agriculteur consulte ses propres parcelles.
        if utilisateur.role == "AGRICULTEUR":
            return parcelles.filter(
                proprietaire=utilisateur
            )

        # L'agronome consulte uniquement les parcelles autorisées.
        if utilisateur.role == "AGRONOME":
            autorisations = AutorisationAcces.objects.filter(
                agronome=utilisateur,
                statut_demande="ACCEPTEE",
                statut_autorisation=StatutAutorisation.ACTIVE,
            )

            autorisations_parcelle = autorisations.filter(
                portee=PorteeAcces.PARCELLE
            ).values_list("parcelle_id", flat=True)

            agriculteurs_toutes = autorisations.filter(
                portee=PorteeAcces.TOUTES,
                parcelle__isnull=True
            ).values_list("agriculteur_id", flat=True)

            return parcelles.filter(
                Q(id__in=autorisations_parcelle)
                |
                Q(proprietaire_id__in=agriculteurs_toutes)
            ).distinct()

        return Parcelle.objects.none()

    def perform_create(self, serializer):

        utilisateur = self.request.user

        if utilisateur.role != "AGRICULTEUR":
            raise PermissionDenied(
                "Seul un agriculteur peut créer une parcelle."
            )

        serializer.save(proprietaire=utilisateur)


class ParcelleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ParcelleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        ParcellePermission,
    ]

    def get_queryset(self):
        return Parcelle.objects.filter(
            date_suppression__isnull=True
        )

    def perform_update(self, serializer):

        if self.request.user.role != "AGRICULTEUR":
            raise PermissionDenied(
                "Seul le propriétaire peut modifier cette parcelle."
            )

        serializer.save()



    def perform_destroy(self, instance):

        if self.request.user.role != "AGRICULTEUR":
            raise PermissionDenied(
                "Seul le propriétaire peut supprimer cette parcelle."
            )

        with transaction.atomic():

            date_suppression = timezone.now()

            # Suppression logique de la parcelle.
            instance.date_suppression = date_suppression
            instance.save(update_fields=["date_suppression"])

            # Révocation des autorisations individuelles actives.
            AutorisationAcces.objects.filter(
                parcelle=instance,
                portee=PorteeAcces.PARCELLE,
                statut_autorisation=StatutAutorisation.ACTIVE
            ).update(
                statut_autorisation=StatutAutorisation.REVOQUEE,
                date_revocation=date_suppression
            )