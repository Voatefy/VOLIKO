from rest_framework import serializers

from .models import CandidatureAgronome, StatutCandidature

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