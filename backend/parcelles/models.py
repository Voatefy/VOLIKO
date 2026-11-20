
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Area
from django.db.models.functions import Cast

class Parcelle(models.Model):
    nom_parcelle = models.CharField(max_length=150)

    geometrie = models.MultiPolygonField(srid=4326)

    superficie = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        editable=False
    )

    date_creation_parcelle = models.DateTimeField(auto_now_add=True)

    date_suppression = models.DateTimeField(
        null=True,
        blank=True
    )

    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="parcelles"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        surface = (
            Parcelle.objects
            .filter(pk=self.pk)
            .annotate(
                surface_calculee=Area(
                    Cast(
                        "geometrie",
                        output_field=models.GeometryField(
                            srid=4326,
                            geography=True
                        )
                    ),
                    spheroid=True
                )
            )
            .values_list("surface_calculee", flat=True)
            .get()
        )

        self.superficie = surface.sq_m

        Parcelle.objects.filter(pk=self.pk).update(
            superficie=self.superficie
        )

    def __str__(self):
        return self.nom_parcelle


class Culture(models.Model):
    nom_culture = models.CharField(max_length=150)

    description_culture = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom_culture


class CultureParcelle(models.Model):
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="cultures_parcelle"
    )

    culture = models.ForeignKey(
        Culture,
        on_delete=models.PROTECT,
        related_name="parcelles_culture"
    )

    date_semis = models.DateField(
        null=True,
        blank=True
    )

    date_fin_culture = models.DateField(
        null=True,
        blank=True
    )

    superficie_occupee = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True
    )

    variete = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            parcelle_db = Parcelle.objects.only(
                "date_suppression"
            ).get(pk=self.parcelle.pk)

            if parcelle_db.date_suppression is not None:
                from django.core.exceptions import ValidationError

                raise ValidationError(
                    "Impossible d'associer une culture "
                    "à une parcelle supprimée."
                )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.culture} - {self.parcelle}"
