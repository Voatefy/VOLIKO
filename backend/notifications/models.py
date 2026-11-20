
from django.conf import settings
from django.db import models


class TypeNotification(models.TextChoices):
    CANDIDATURE = "CANDIDATURE", "Candidature"
    ACCES = "ACCES", "Accès aux parcelles"
    RECOMMANDATION = "RECOMMANDATION", "Recommandation"
    ACTIVITE = "ACTIVITE", "Activité agricole"
    ALERTE = "ALERTE", "Alerte agricole"
    ANALYSE = "ANALYSE", "Analyse agricole"


class CanalNotification(models.TextChoices):
    APPLICATION = "APPLICATION", "Application"
    EMAIL = "EMAIL", "E-mail"


class Notification(models.Model):
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="notifications"
    )
    contenu = models.TextField()
    type_notification = models.CharField(
        max_length=30,
        choices=TypeNotification.choices
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_type_notification_display()} - {self.destinataire}"


class PreferenceNotification(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preferences_notifications"
    )
    categorie_notification = models.CharField(
        max_length=30,
        choices=TypeNotification.choices
    )
    canal = models.CharField(
        max_length=20,
        choices=CanalNotification.choices
    )
    est_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "utilisateur",
                    "categorie_notification",
                    "canal"
                ],
                name="une_preference_par_utilisateur_categorie_canal"
            )
        ]

    def __str__(self):
        return (
            f"{self.utilisateur} - "
            f"{self.categorie_notification} - {self.canal}"
        )
