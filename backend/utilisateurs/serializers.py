from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Utilisateur


class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = Utilisateur
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        utilisateur = Utilisateur.objects.create_user(
            password=password,
            **validated_data
        )

        return utilisateur


class ProfilUtilisateurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Utilisateur
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        ]

        read_only_fields = ["id", "username", "role"]
