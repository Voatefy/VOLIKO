from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):

    class Role(models.TextChoices):
        AGRICULTEUR = "AGRICULTEUR", "Agriculteur"
        CANDIDAT_AGRONOME = "CANDIDAT_AGRONOME", "Candidat agronome"
        AGRONOME = "AGRONOME", "Agronome"
        ADMINISTRATEUR = "ADMINISTRATEUR", "Administrateur"

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.AGRICULTEUR
    )

    def __str__(self):
        return f"{self.username} ({self.role})"