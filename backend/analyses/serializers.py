
from rest_framework import serializers

from .models import (
    ObservationNDVI,
    DonneeMeteo,
    AlerteAgricole,
    ConseilAgricole,
)


class ObservationNDVISerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationNDVI
        fields = "__all__"
        read_only_fields = (
            "id",
            "parcelle",
            "valeur_ndvi",
            "date_acquisition_image",
            "date_traitement",
            "couverture_nuageuse",
            "source_image",
            "qualite_donnees",
        )


class DonneeMeteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonneeMeteo
        fields = "__all__"
        read_only_fields = (
            "id",
            "parcelle",
            "date_meteo",
            "temperature",
            "precipitation",
            "humidite",
            "source_meteo",
            "date_recuperation",
        )


class AlerteAgricoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlerteAgricole
        fields = "__all__"
        read_only_fields = (
            "id",
            "parcelle",
            "type_alerte",
            "niveau_alerte",
            "contenu_alerte",
            "date_alerte",
        )


class ConseilAgricoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConseilAgricole
        fields = "__all__"
        read_only_fields = (
            "id",
            "parcelle",
            "contenu_conseil",
            "source_conseil",
            "date_generation",
        )
