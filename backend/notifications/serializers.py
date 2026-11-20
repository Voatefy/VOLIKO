
from rest_framework import serializers

from .models import Notification, PreferenceNotification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            "id",
            "contenu",
            "type_notification",
            "date_creation",
            "date_lecture",
        ]
        read_only_fields = fields

class PreferenceNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreferenceNotification
        fields = [
            "id",
            "categorie_notification",
            "canal",
            "est_active",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        utilisateur = self.context["request"].user

        categorie = attrs.get(
            "categorie_notification",
            getattr(self.instance, "categorie_notification", None),
        )
        canal = attrs.get(
            "canal",
            getattr(self.instance, "canal", None),
        )

        queryset = PreferenceNotification.objects.filter(
            utilisateur=utilisateur,
            categorie_notification=categorie,
            canal=canal,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Cette préférence de notification existe déjà."
            )

        return attrs