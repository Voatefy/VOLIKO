
from django.db.models import Q

from rest_framework import generics, permissions

from collaborations.models import (
    AutorisationAcces,
    PorteeAcces,
    StatutAutorisation,
)
from utilisateurs.models import Utilisateur

from .models import (
    ObservationNDVI,
    DonneeMeteo,
    AlerteAgricole,
    ConseilAgricole,
)
from .serializers import (
    ObservationNDVISerializer,
    DonneeMeteoSerializer,
    AlerteAgricoleSerializer,
    ConseilAgricoleSerializer,
)


def parcelles_accessibles(utilisateur):
    """
    Agriculteur : ses parcelles, y compris supprimées.
    Agronome : uniquement les parcelles actives autorisées.
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
            portee=PorteeAcces.PARCELLE,
            parcelle__date_suppression__isnull=True,
        ).values_list("parcelle_id", flat=True)

        agriculteurs_toutes = autorisations.filter(
            portee=PorteeAcces.TOUTES,
            parcelle__isnull=True,
        ).values_list("agriculteur_id", flat=True)

        return (
            Q(parcelle_id__in=parcelles_individuelles)
            | Q(
                parcelle__proprietaire_id__in=agriculteurs_toutes,
                parcelle__date_suppression__isnull=True,
            )
        )

    return Q(pk__in=[])


class AnalyseListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            parcelles_accessibles(self.request.user)
        ).select_related("parcelle")


class AnalyseDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            parcelles_accessibles(self.request.user)
        ).select_related("parcelle")


class ObservationNDVIListAPIView(AnalyseListAPIView):
    serializer_class = ObservationNDVISerializer
    queryset = ObservationNDVI.objects.all()


class ObservationNDVIDetailAPIView(AnalyseDetailAPIView):
    serializer_class = ObservationNDVISerializer
    queryset = ObservationNDVI.objects.all()


class DonneeMeteoListAPIView(AnalyseListAPIView):
    serializer_class = DonneeMeteoSerializer
    queryset = DonneeMeteo.objects.all()


class DonneeMeteoDetailAPIView(AnalyseDetailAPIView):
    serializer_class = DonneeMeteoSerializer
    queryset = DonneeMeteo.objects.all()


class AlerteAgricoleListAPIView(AnalyseListAPIView):
    serializer_class = AlerteAgricoleSerializer
    queryset = AlerteAgricole.objects.all()


class AlerteAgricoleDetailAPIView(AnalyseDetailAPIView):
    serializer_class = AlerteAgricoleSerializer
    queryset = AlerteAgricole.objects.all()


class ConseilAgricoleListAPIView(AnalyseListAPIView):
    serializer_class = ConseilAgricoleSerializer
    queryset = ConseilAgricole.objects.all()


class ConseilAgricoleDetailAPIView(AnalyseDetailAPIView):
    serializer_class = ConseilAgricoleSerializer
    queryset = ConseilAgricole.objects.all()
