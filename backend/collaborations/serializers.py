from .models import (
    CandidatureAgronome,
    DocumentCandidature,
    StatutCandidature,
    AutorisationAcces,
    PorteeAcces,
    StatutDemandeAcces,
    StatutAutorisation,
)

from rest_framework import serializers

class CandidatureAgronomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidatureAgronome
        fields = [
            "id",
            "candidat",
            "administrateur",
            "date_candidature",
            "statut",
            "diplome",
            "experience",
            "motif_decision",
            "date_decision",
        ]

        read_only_fields = [
            "id",
            "candidat",
            "administrateur",
            "date_candidature",
            "statut",
            "motif_decision",
            "date_decision",
        ]

    def validate(self, attrs):
        if self.instance and self.instance.statut in [
            StatutCandidature.ACCEPTEE,
            StatutCandidature.REJETEE,
        ]:
            raise serializers.ValidationError(
                "Cette candidature ne peut plus être modifiée."
            )

        return attrs

class CandidatureAgronomeAdminSerializer(serializers.ModelSerializer):

    candidat = serializers.SerializerMethodField()

    administrateur = serializers.StringRelatedField()

    class Meta:
        model = CandidatureAgronome
        fields = [
            "id",
            "candidat",
            "administrateur",
            "date_candidature",
            "statut",
            "diplome",
            "experience",
            "motif_decision",
            "date_decision",
        ]

    def get_candidat(self, obj):
        return {
            "id": obj.candidat.id,
            "username": obj.candidat.username,
            "first_name": obj.candidat.first_name,
            "last_name": obj.candidat.last_name,
            "email": obj.candidat.email,
            "role": obj.candidat.role,
        }


class DecisionCandidatureSerializer(serializers.Serializer):

    statut = serializers.ChoiceField(
        choices=[
            StatutCandidature.ACCEPTEE,
            StatutCandidature.REJETEE,
        ]
    )

    motif_decision = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate(self, attrs):
        if (
            attrs["statut"] == StatutCandidature.REJETEE
            and not attrs.get("motif_decision", "").strip()
        ):
            raise serializers.ValidationError({
                "motif_decision": "Le motif du rejet est obligatoire."
            })

        return attrs


class DocumentCandidatureUploadSerializer(serializers.ModelSerializer):

    fichier = serializers.FileField(
        write_only=True,
        source="chemin_stockage"
    )

    class Meta:
        model = DocumentCandidature
        fields = [
            "id",
            "type_document",
            "fichier",
            "nom_fichier",
            "date_ajout",
        ]
        read_only_fields = [
            "id",
            "nom_fichier",
            "date_ajout",
        ]

    def validate_fichier(self, fichier):
        extensions_autorisees = [
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
        ]

        nom = fichier.name.lower()
        extension = "." + nom.rsplit(".", 1)[-1] if "." in nom else ""

        if extension not in extensions_autorisees:
            raise serializers.ValidationError(
                "Format non autorisé. Utilisez PDF, JPG ou PNG."
            )

        if fichier.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "La taille du fichier ne doit pas dépasser 5 Mo."
            )

        return fichier

    def create(self, validated_data):
        fichier = validated_data["chemin_stockage"]

        validated_data["nom_fichier"] = (
            fichier.name.replace("\\", "/").split("/")[-1][:255]
        )

        return super().create(validated_data)



class DocumentCandidatureReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentCandidature
        fields = [
            "id",
            "type_document",
            "nom_fichier",
            "date_ajout",
        ]
        read_only_fields = fields



class AutorisationAccesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AutorisationAcces
        fields = [
            "id",
            "agriculteur",
            "agronome",
            "portee",
            "parcelle",
            "types_donnees",
            "date_demande",
            "statut_demande",
            "date_decision",
            "statut_autorisation",
            "date_autorisation",
            "date_revocation",
            "motif_demande",
        ]

        read_only_fields = [
            "id",
            "agronome",
            "date_demande",
            "statut_demande",
            "date_decision",
            "statut_autorisation",
            "date_autorisation",
            "date_revocation",
        ]

    def validate(self, attrs):

        utilisateur = self.context["request"].user

        if utilisateur.role != "AGRONOME":
            raise serializers.ValidationError(
                "Seul un agronome peut demander une autorisation."
            )

        agriculteur = attrs.get(
            "agriculteur",
            self.instance.agriculteur if self.instance else None
        )

        if not agriculteur or agriculteur.role != "AGRICULTEUR":
            raise serializers.ValidationError({
                "agriculteur": "L'utilisateur sélectionné doit être un agriculteur."
            })

        portee = attrs.get(
            "portee",
            self.instance.portee if self.instance else None
        )

        parcelle = attrs.get(
            "parcelle",
            self.instance.parcelle if self.instance else None
        )

        if portee == PorteeAcces.PARCELLE:

            if not parcelle:
                raise serializers.ValidationError({
                    "parcelle": "Une parcelle doit être sélectionnée."
                })

            if parcelle.proprietaire_id != agriculteur.id:
                raise serializers.ValidationError({
                    "parcelle": "Cette parcelle n'appartient pas à cet agriculteur."
                })

            if parcelle.date_suppression is not None:
                raise serializers.ValidationError({
                    "parcelle": "Cette parcelle est supprimée."
                })

        elif portee == PorteeAcces.TOUTES:

            if parcelle:
                raise serializers.ValidationError({
                    "parcelle": "La portée TOUTES ne doit pas cibler une parcelle."
                })

        return attrs

    def create(self, validated_data):

        validated_data["agronome"] = self.context["request"].user

        return super().create(validated_data)


class DecisionAutorisationSerializer(serializers.Serializer):

    statut = serializers.ChoiceField(
        choices=[
            StatutDemandeAcces.ACCEPTEE,
            StatutDemandeAcces.REFUSEE,
        ]
    )

    motif_decision = serializers.CharField(
        required=False,
        allow_blank=True
    )