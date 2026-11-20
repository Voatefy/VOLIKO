from utilisateurs.models import Utilisateur
from rest_framework import serializers

from .models import (
    ActivitePlanifiee,
    ActiviteAgricole,
    StatutActivitePlanifiee,
)


class ActivitePlanifieeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivitePlanifiee
        fields = [
            "id",
            "parcelle",
            "type_activite",
            "date_prevue",
            "statut",
            "date_report",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        instance = self.instance
        request = self.context.get("request")

        if request and request.user.role != Utilisateur.Role.AGRICULTEUR:
            return attrs

        parcelle = attrs.get(
            "parcelle",
            instance.parcelle if instance else None
        )

        statut = attrs.get(
            "statut",
            instance.statut if instance else StatutActivitePlanifiee.PLANIFIEE
        )

        date_report = attrs.get(
            "date_report",
            instance.date_report if instance else None
        )

        if parcelle:
            if parcelle.date_suppression is not None:
                raise serializers.ValidationError({
                    "parcelle": "Cette parcelle est supprimée."
                })

            if request and parcelle.proprietaire_id != request.user.id:
                raise serializers.ValidationError({
                    "parcelle": "Vous ne pouvez pas planifier une activité sur cette parcelle."
                })

        if statut == StatutActivitePlanifiee.REPORTEE and date_report is None:
            raise serializers.ValidationError({
                "date_report": "Une nouvelle date est obligatoire pour reporter une activité."
            })

        if statut != StatutActivitePlanifiee.REPORTEE and date_report is not None:
            raise serializers.ValidationError({
                "date_report": "La date de report doit être renseignée uniquement pour une activité reportée."
            })

        return attrs


class ActiviteAgricoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiviteAgricole
        fields = [
            "id",
            "parcelle",
            "activite_planifiee",
            "type_activite",
            "date_activite",
            "description",
            "intrant",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        instance = self.instance
        request = self.context.get("request")

        if request and request.user.role != Utilisateur.Role.AGRICULTEUR:
            return attrs

        parcelle = attrs.get(
            "parcelle",
            instance.parcelle if instance else None
        )

        activite_planifiee = attrs.get(
            "activite_planifiee",
            instance.activite_planifiee if instance else None
        )

        type_activite = attrs.get(
            "type_activite",
            instance.type_activite if instance else None
        )

        if parcelle:
            if parcelle.date_suppression is not None:
                raise serializers.ValidationError({
                    "parcelle": "Cette parcelle est supprimée."
                })

            if request and parcelle.proprietaire_id != request.user.id:
                raise serializers.ValidationError({
                    "parcelle": "Vous ne pouvez pas enregistrer une activité sur cette parcelle."
                })

        if parcelle and activite_planifiee:

            if activite_planifiee.parcelle_id != parcelle.id:
                raise serializers.ValidationError({
                    "activite_planifiee": "L'activité planifiée doit appartenir à la même parcelle."
                })

            if activite_planifiee.statut in [
                StatutActivitePlanifiee.ANNULEE,
                StatutActivitePlanifiee.TERMINEE,
            ]:
                raise serializers.ValidationError({
                    "activite_planifiee": "Cette activité planifiée ne peut plus être réalisée."
                })

            if activite_planifiee.type_activite != type_activite:
                raise serializers.ValidationError({
                    "type_activite": "Le type doit correspondre à celui de l'activité planifiée."
                })

        return attrs
