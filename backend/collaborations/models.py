
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from parcelles.models import Parcelle


# ==================================================
# 1. CANDIDATURE D'UN AGRONOME
# ==================================================

def verifier_parcelle_active(parcelle):
    parcelle_db = Parcelle.objects.only(
        "date_suppression"
    ).get(pk=parcelle.pk)

    if parcelle_db.date_suppression is not None:
        raise ValidationError(
            "Impossible de créer une demande ou une recommandation "
            "pour une parcelle supprimée."
        )

class StatutCandidature(models.TextChoices):
    BROUILLON = "BROUILLON", "Brouillon"
    SOUMISE = "SOUMISE", "Soumise"
    EN_EXAMEN = "EN_EXAMEN", "En examen"
    A_CORRIGER = "A_CORRIGER", "À corriger"
    ACCEPTEE = "ACCEPTEE", "Acceptée"
    REJETEE = "REJETEE", "Rejetée"


class CandidatureAgronome(models.Model):
    candidat = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="candidatures_agronome"
    )

    administrateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="candidatures_examinees",
        null=True,
        blank=True
    )

    date_candidature = models.DateTimeField(
        null=True,
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutCandidature.choices,
        default=StatutCandidature.BROUILLON
    )

    diplome = models.CharField(max_length=255)

    experience = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    motif_decision = models.TextField(
        null=True,
        blank=True
    )

    date_decision = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candidat"],
                condition=Q(
                    statut__in=[
                        "BROUILLON",
                        "SOUMISE",
                        "EN_EXAMEN",
                        "A_CORRIGER"
                    ]
                ),
                name="une_candidature_non_terminee_par_candidat"
            )
        ]

    def __str__(self):
        return f"Candidature - {self.candidat} - {self.statut}"


# ==================================================
# 2. DOCUMENTS DE CANDIDATURE
# ==================================================

class DocumentCandidature(models.Model):
    candidature = models.ForeignKey(
        CandidatureAgronome,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    nom_fichier = models.CharField(max_length=255)

    type_document = models.CharField(max_length=100)

    chemin_stockage = models.FileField(
        upload_to="candidatures/"
    )

    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_document} - {self.nom_fichier}"


# ==================================================
# 3. DEMANDE DE RECOMMANDATION
# ==================================================

class StatutDemandeRecommandation(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", "En attente"
    ACCEPTEE = "ACCEPTEE", "Acceptée"
    REFUSEE = "REFUSEE", "Refusée"


class DemandeRecommandation(models.Model):
    agriculteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="demandes_recommandation"
    )

    agronome = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="demandes_recues"
    )

    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="demandes_recommandation"
    )

    description = models.TextField()

    date_demande = models.DateTimeField(auto_now_add=True)

    statut = models.CharField(
        max_length=20,
        choices=StatutDemandeRecommandation.choices,
        default=StatutDemandeRecommandation.EN_ATTENTE
    )

    date_traitement = models.DateTimeField(
        null=True,
        blank=True
    )

    motif_decision = models.TextField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Demande - {self.parcelle} - {self.statut}"


# ==================================================
# 4. AUTORISATION D'ACCES
# ==================================================

class PorteeAcces(models.TextChoices):
    PARCELLE = "PARCELLE", "Une parcelle"
    TOUTES = "TOUTES", "Toutes les parcelles"


class StatutDemandeAcces(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", "En attente"
    ACCEPTEE = "ACCEPTEE", "Acceptée"
    REFUSEE = "REFUSEE", "Refusée"


class StatutAutorisation(models.TextChoices):
    INACTIVE = "INACTIVE", "Non active"
    ACTIVE = "ACTIVE", "Active"
    REVOQUEE = "REVOQUEE", "Révoquée"


class AutorisationAcces(models.Model):
    agriculteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="autorisations_accordees"
    )

    agronome = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="autorisations_recues"
    )

    portee = models.CharField(
        max_length=20,
        choices=PorteeAcces.choices
    )

    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="autorisations_acces",
        null=True,
        blank=True
    )

    types_donnees = models.JSONField(default=list)

    date_demande = models.DateTimeField(auto_now_add=True)

    statut_demande = models.CharField(
        max_length=20,
        choices=StatutDemandeAcces.choices,
        default=StatutDemandeAcces.EN_ATTENTE
    )

    date_decision = models.DateTimeField(
        null=True,
        blank=True
    )

    statut_autorisation = models.CharField(
        max_length=20,
        choices=StatutAutorisation.choices,
        default=StatutAutorisation.INACTIVE
    )

    date_autorisation = models.DateTimeField(
        null=True,
        blank=True
    )

    date_revocation = models.DateTimeField(
        null=True,
        blank=True
    )

    motif_demande = models.TextField(
        null=True,
        blank=True
    )

    def clean(self):
        super().clean()

        if self.portee == PorteeAcces.PARCELLE and not self.parcelle_id:
            raise ValidationError({
                "parcelle": "Une parcelle doit être sélectionnée."
            })

        if self.portee == PorteeAcces.TOUTES and self.parcelle_id:
            raise ValidationError({
                "parcelle": "La portée TOUTES ne doit pas cibler une parcelle unique."
            })

        if (
            self.parcelle_id
            and self.agriculteur_id
            and self.parcelle.proprietaire_id != self.agriculteur_id
        ):
            raise ValidationError({
                "parcelle": "Cette parcelle n'appartient pas à cet agriculteur."
            })

        
        if (
            self.portee == PorteeAcces.PARCELLE
            and self.parcelle_id
            and self.parcelle.date_suppression is not None
        ):
            raise ValidationError({
                "parcelle": "Impossible d'autoriser l'accès à une parcelle supprimée."
            })
        
    def __str__(self):
        return f"Accès - {self.agronome} - {self.portee}"


# ==================================================
# 5. RECOMMANDATION AGRICOLE
# ==================================================

class StatutRecommandation(models.TextChoices):
    BROUILLON = "BROUILLON", "Brouillon"
    TRANSMISE = "TRANSMISE", "Transmise"


class RecommandationAgricole(models.Model):
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="recommandations_redigees"
    )

    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="recommandations_recues"
    )

    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.PROTECT,
        related_name="recommandations_agricoles"
    )

    demande = models.ForeignKey(
        DemandeRecommandation,
        on_delete=models.PROTECT,
        related_name="recommandations",
        null=True,
        blank=True
    )

    titre = models.CharField(max_length=255)

    contenu = models.TextField(blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    date_transmission = models.DateTimeField(
        null=True,
        blank=True
    )

    date_consultation = models.DateTimeField(
        null=True,
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutRecommandation.choices,
        default=StatutRecommandation.BROUILLON
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            verifier_parcelle_active(self.parcelle)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} - {self.parcelle}"
