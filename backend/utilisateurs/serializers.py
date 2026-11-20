from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

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

class ConnexionEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        utilisateur = Utilisateur.objects.filter(
            email__iexact=email
        ).first()

        if not utilisateur or not utilisateur.check_password(password):
            raise AuthenticationFailed("Identifiants invalides.")

        if not utilisateur.is_active:
            raise AuthenticationFailed(
                "Votre compte est désactivé. Veuillez contacter l'administrateur."
            )

        refresh = RefreshToken.for_user(utilisateur)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }