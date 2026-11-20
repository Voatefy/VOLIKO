
from django.db import models
from django.db.models import Q
from parcelles.models import Parcelle
from django.core.exceptions import ValidationError


def verifier_parcelle_active(parcelle):
    parcelle_db = Parcelle.objects.only(
        "date_suppression"
    ).get(pk=parcelle.pk)

    if parcelle_db.date_suppression is not None:
        raise ValidationError(
            "Impossible de créer une nouvelle donnée "
            "pour une parcelle supprimée."
        )

class ObservationNDVI(models.Model):
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="observations_ndvi"
    )

    valeur_ndvi = models.DecimalField(
        max_digits=5,
        decimal_places=4
    )

    date_acquisition_image = models.DateTimeField()
    date_traitement = models.DateTimeField()

    couverture_nuageuse = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    source_image = models.CharField(max_length=255)

    qualite_donnees = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(valeur_ndvi__gte=-1) & Q(valeur_ndvi__lte=1),
                name="ndvi_valeur_entre_moins1_et_1"
            ),
            models.CheckConstraint(
                condition=(
                    Q(couverture_nuageuse__isnull=True)
                    | (
                        Q(couverture_nuageuse__gte=0)
                        & Q(couverture_nuageuse__lte=100)
                    )
                ),
                name="ndvi_couverture_entre_0_et_100"
            )
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"NDVI - {self.parcelle} - {self.date_acquisition_image}"


class DonneeMeteo(models.Model):
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="donnees_meteo"
    )

    date_meteo = models.DateTimeField()

    temperature = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    precipitation = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    humidite = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    source_meteo = models.CharField(max_length=100)
    date_recuperation = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(precipitation__isnull=True)
                    | Q(precipitation__gte=0)
                ),
                name="meteo_precipitation_positive"
            ),
            models.CheckConstraint(
                condition=(
                    Q(humidite__isnull=True)
                    | (
                        Q(humidite__gte=0)
                        & Q(humidite__lte=100)
                    )
                ),
                name="meteo_humidite_entre_0_et_100"
            )
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Météo - {self.parcelle} - {self.date_meteo}"


class TypeAlerte(models.TextChoices):
    VEGETATION = "VEGETATION", "Végétation"
    METEO = "METEO", "Météo"
    AUTRE = "AUTRE", "Autre"


class NiveauAlerte(models.TextChoices):
    FAIBLE = "FAIBLE", "Faible"
    MOYEN = "MOYEN", "Moyen"
    ELEVE = "ELEVE", "Élevé"
    CRITIQUE = "CRITIQUE", "Critique"


class AlerteAgricole(models.Model):
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="alertes_agricoles"
    )

    type_alerte = models.CharField(
        max_length=20,
        choices=TypeAlerte.choices
    )

    niveau_alerte = models.CharField(
        max_length=20,
        choices=NiveauAlerte.choices
    )

    contenu_alerte = models.TextField()
    date_alerte = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_alerte} - {self.parcelle}"


class SourceConseil(models.TextChoices):
    IA = "IA", "Intelligence artificielle"
    REGLES_METIER = "REGLES_METIER", "Règles métier"


class ConseilAgricole(models.Model):
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="conseils_agricoles"
    )

    contenu_conseil = models.TextField()

    source_conseil = models.CharField(
        max_length=20,
        choices=SourceConseil.choices
    )

    date_generation = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Conseil - {self.parcelle} - {self.source_conseil}"
