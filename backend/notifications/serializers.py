
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
