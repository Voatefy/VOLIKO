from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Parcelle, Culture, CultureParcelle
from rest_framework_gis.fields import GeometryField




class CultureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Culture
        fields = [
            "id",
            "nom_culture",
            "description_culture",
        ]



class CultureParcelleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CultureParcelle
        fields = [
            "id",
            "parcelle",
            "culture",
            "date_semis",
            "date_fin_culture",
            "superficie_occupee",
            "variete",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        instance = self.instance

        parcelle = attrs.get(
            "parcelle",
            instance.parcelle if instance else None
        )

        date_semis = attrs.get(
            "date_semis",
            instance.date_semis if instance else None
        )

        date_fin = attrs.get(
            "date_fin_culture",
            instance.date_fin_culture if instance else None
        )

        superficie = attrs.get(
            "superficie_occupee",
            instance.superficie_occupee if instance else None
        )

        if parcelle and parcelle.date_suppression is not None:
            raise serializers.ValidationError({
                "parcelle": "Cette parcelle est supprimée."
            })

        if date_semis and date_fin and date_fin < date_semis:
            raise serializers.ValidationError({
                "date_fin_culture":
                    "La date de fin ne peut pas précéder la date de semis."
            })

        # ==

        if superficie is not None and superficie < 0:
            raise serializers.ValidationError({
                "superficie_occupee":
                    "La superficie occupée ne peut pas être négative."
            })

        # ==

        if (
            parcelle
            and superficie is not None
            and superficie > parcelle.superficie
        ):
            raise serializers.ValidationError({
                "superficie_occupee":
                    "La superficie occupée dépasse celle de la parcelle."
            })

        return attrs



class ParcelleSerializer(GeoFeatureModelSerializer):

    geometrie = GeometryField()

    class Meta:
        model = Parcelle
        geo_field = "geometrie"
        fields = [
            "id",
            "nom_parcelle",
            "geometrie",
            "superficie",
            "date_creation_parcelle",
            "proprietaire",
        ]

        read_only_fields = [
            "id",
            "superficie",
            "date_creation_parcelle",
            "proprietaire",
        ]