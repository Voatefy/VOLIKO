from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Parcelle, Culture, CultureParcelle
from rest_framework_gis.fields import GeometryField


class ParcelleSerializer(GeoFeatureModelSerializer):

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