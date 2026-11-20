
from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from collaborations.models import (
    AutorisationAcces,
    PorteeAcces,
    StatutAutorisation,
)
from utilisateurs.models import Utilisateur

from .models import ActivitePlanifiee, ActiviteAgricole
from .serializers import (
    ActivitePlanifieeSerializer,
    ActiviteAgricoleSerializer,
)


def parcelles_accessibles(utilisateur):
    """
    Retourne les parcelles appartenant à l'agriculteur
    ou accessibles en lecture à l'agronome.
    """

    if utilisateur.role == Utilisateur.Role.AGRICULTEUR:
        return Q(parcelle__proprietaire=utilisateur)

    if utilisateur.role == Utilisateur.Role.AGRONOME:

        autorisations = AutorisationAcces.objects.filter(
            agronome=utilisateur,
            statut_demande="ACCEPTEE",
            statut_autorisation=StatutAutorisation.ACTIVE,
        )

        parcelles_individuelles = autorisations.filter(
            portee=PorteeAcces.PARCELLE
        ).values_list("parcelle_id", flat=True)

        agriculteurs_toutes = autorisations.filter(
            portee=PorteeAcces.TOUTES,
            parcelle__isnull=True
        ).values_list("agriculteur_id", flat=True)

        return (
            Q(parcelle_id__in=parcelles_individuelles)
            | Q(parcelle__proprietaire_id__in=agriculteurs_toutes)
        )

    return Q(pk__in=[])


class ActivitePlanifieeListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ActivitePlanifieeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivitePlanifiee.objects.filter(
            parcelles_accessibles(self.request.user)
        ).select_related("parcelle")

    def perform_create(self, serializer):

        if self.request.user.role != Utilisateur.Role.AGRICULTEUR:
            raise PermissionDenied(
                "Seul un agriculteur peut planifier une activité."
            )

        serializer.save()


class ActivitePlanifieeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ActivitePlanifieeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivitePlanifiee.objects.filter(
            parcelles_accessibles(self.request.user)
        ).select_related("parcelle")

    def perform_update(self, serializer):

        if self.request.user.role != Utilisateur.Role.AGRICULTEUR:
            raise PermissionDenied(
                "Seul l'agriculteur propriétaire peut modifier cette activité."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if self.request.user.role != Utilisateur.Role.AGRICULTEUR:
            raise PermissionDenied(
                "Seul l'agriculteur propriétaire peut supprimer cette activité."
            )

        instance.delete()


class ActiviteAgricoleListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ActiviteAgricoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActiviteAgricole.objects.filter(
            parcelles_accessibles(self.request.user)
        ).select_related("parcelle", "activite_planifiee")

    def perform_create(self, serializer):

        if self.request.user.role != Utilisateur.Role.AGRICULTEUR:
            raise PermissionDenied(
                "Seul un agriculteur peut enregistrer une activité réalisée."
            )

        serializer.save()


class ActiviteAgricoleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ActiviteAgricoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActiviteAgricole.objects.filter(
            parcelles_accessibles(self.request.user)
        ).select_related("parcelle", "activite_planifiee")

    def perform_update(self, serializer):

        if self.request.user.role != Utilisateur.Role.AGRICULTEUR:
            raise PermissionDenied(
                "Seul l'agriculteur propriétaire peut modifier cette activité."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if self.request.user.role != Utilisateur.Role.AGRICULTEUR:
            raise PermissionDenied(
                "Seul l'agriculteur propriétaire peut supprimer cette activité."
            )

        instance.delete()
