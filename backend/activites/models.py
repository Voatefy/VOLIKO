from django.db import models
from parcelles.models import Parcelle
from django.core.exceptions import ValidationError


def verifier_parcelle_active(parcelle):
    parcelle_db = Parcelle.objects.only(
        "date_suppression"
    ).get(pk=parcelle.pk)

    if parcelle_db.date_suppression is not None:
        raise ValidationError(
            "Impossible de créer une activité "
            "pour une parcelle supprimée."
        )

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

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_activite_display()} - {self.parcelle}"
