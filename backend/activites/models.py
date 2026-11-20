from django.db import models
from parcelles.models import Parcelle


class TypeActivite(models.TextChoices):
    SEMIS = "SEMIS", "Semis"
    IRRIGATION = "IRRIGATION", "Irrigation"
    FERTILISATION = "FERTILISATION", "Fertilisation"
    TRAITEMENT = "TRAITEMENT", "Traitement"
    RECOLTE = "RECOLTE", "Récolte"
    AUTRE = "AUTRE", "Autre"


class StatutActivitePlanifiee(models.TextChoices):
    PLANIFIEE = "PLANIFIEE", "Planifiée"
    EN_RETARD = "EN_RETARD", "En retard"
    TERMINEE = "TERMINEE", "Terminée"
    REPORTEE = "REPORTEE", "Reportée"
    ANNULEE = "ANNULEE", "Annulée"


class ActivitePlanifiee(models.Model):
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="activites_planifiees"
    )

    type_activite = models.CharField(
        max_length=20,
        choices=TypeActivite.choices
    )

    date_prevue = models.DateTimeField()

    statut = models.CharField(
        max_length=20,
        choices=StatutActivitePlanifiee.choices,
        default=StatutActivitePlanifiee.PLANIFIEE
    )

    date_report = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.get_type_activite_display()} - {self.parcelle}"


class ActiviteAgricole(models.Model):
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="activites_agricoles"
    )

    activite_planifiee = models.OneToOneField(
        ActivitePlanifiee,
        on_delete=models.PROTECT,
        related_name="activite_realisee",
        null=True,
        blank=True
    )

    type_activite = models.CharField(
        max_length=20,
        choices=TypeActivite.choices
    )

    date_activite = models.DateTimeField()

    description = models.TextField(
        null=True,
        blank=True
    )

    intrant = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.get_type_activite_display()} - {self.parcelle}"
