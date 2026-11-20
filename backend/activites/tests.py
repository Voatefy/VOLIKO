
from datetime import timedelta

from django.contrib.gis.geos import MultiPolygon, Polygon
from django.utils import timezone

from rest_framework.test import APITestCase

from utilisateurs.models import Utilisateur
from parcelles.models import Parcelle
from collaborations.models import (
    AutorisationAcces,
    PorteeAcces,
    StatutDemandeAcces,
    StatutAutorisation,
)
from .models import ActivitePlanifiee, ActiviteAgricole


class ActivitesHistoriqueTests(APITestCase):

    def setUp(self):
        self.agriculteur = Utilisateur.objects.create_user(
            username="agriculteur_test",
            password="test123",
            role=Utilisateur.Role.AGRICULTEUR,
        )

        self.agronome = Utilisateur.objects.create_user(
            username="agronome_test",
            password="test123",
            role=Utilisateur.Role.AGRONOME,
        )

        polygon = Polygon((
            (47.5, -18.9),
            (47.501, -18.9),
            (47.501, -18.901),
            (47.5, -18.901),
            (47.5, -18.9),
        ))

        geometrie = MultiPolygon(polygon, srid=4326)

        self.parcelle = Parcelle.objects.create(
            nom_parcelle="Parcelle test historique",
            geometrie=geometrie,
            proprietaire=self.agriculteur,
        )

        self.planifiee = ActivitePlanifiee.objects.create(
            parcelle=self.parcelle,
            type_activite="SEMIS",
            date_prevue=timezone.now() + timedelta(days=2),
        )

        self.realisee = ActiviteAgricole.objects.create(
            parcelle=self.parcelle,
            activite_planifiee=self.planifiee,
            type_activite="SEMIS",
            date_activite=timezone.now(),
            description="Activité historique de test",
        )

        # Suppression logique de la parcelle.
        Parcelle.objects.filter(pk=self.parcelle.pk).update(
            date_suppression=timezone.now()
        )

        self.parcelle.refresh_from_db()

        # Autorisation globale toujours active.
        AutorisationAcces.objects.create(
            agriculteur=self.agriculteur,
            agronome=self.agronome,
            portee=PorteeAcces.TOUTES,
            statut_demande=StatutDemandeAcces.ACCEPTEE,
            statut_autorisation=StatutAutorisation.ACTIVE,
        )

    def test_agriculteur_peut_consulter_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        response_planifiees = self.client.get("/api/activites/")
        response_realisees = self.client.get(
            "/api/activites/realisees/"
        )

        self.assertEqual(response_planifiees.status_code, 200)
        self.assertEqual(response_realisees.status_code, 200)

        self.assertTrue(
            any(
                item["id"] == self.planifiee.id
                for item in response_planifiees.data
            )
        )

        self.assertTrue(
            any(
                item["id"] == self.realisee.id
                for item in response_realisees.data
            )
        )

    def test_agriculteur_peut_consulter_details_historiques(self):
        self.client.force_authenticate(user=self.agriculteur)

        response_planifiee = self.client.get(
            f"/api/activites/{self.planifiee.id}/"
        )

        response_realisee = self.client.get(
            f"/api/activites/realisees/{self.realisee.id}/"
        )

        self.assertEqual(response_planifiee.status_code, 200)
        self.assertEqual(response_realisee.status_code, 200)

    def test_agriculteur_ne_peut_pas_modifier_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        response_planifiee = self.client.patch(
            f"/api/activites/{self.planifiee.id}/",
            {"statut": "ANNULEE"},
            format="json",
        )

        response_realisee = self.client.patch(
            f"/api/activites/realisees/{self.realisee.id}/",
            {"description": "Modification interdite"},
            format="json",
        )

        self.assertIn(response_planifiee.status_code, [400, 403])
        self.assertIn(response_realisee.status_code, [400, 403])

    def test_agriculteur_ne_peut_pas_supprimer_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        response_planifiee = self.client.delete(
            f"/api/activites/{self.planifiee.id}/"
        )

        response_realisee = self.client.delete(
            f"/api/activites/realisees/{self.realisee.id}/"
        )

        self.assertEqual(response_planifiee.status_code, 403)
        self.assertEqual(response_realisee.status_code, 403)

        self.assertTrue(
            ActivitePlanifiee.objects.filter(
                pk=self.planifiee.pk
            ).exists()
        )

        self.assertTrue(
            ActiviteAgricole.objects.filter(
                pk=self.realisee.pk
            ).exists()
        )

    def test_agronome_ne_peut_pas_consulter_historique(self):
        self.client.force_authenticate(user=self.agronome)

        response_planifiees = self.client.get("/api/activites/")
        response_realisees = self.client.get(
            "/api/activites/realisees/"
        )

        self.assertEqual(response_planifiees.status_code, 200)
        self.assertEqual(response_realisees.status_code, 200)

        self.assertFalse(
            any(
                item["id"] == self.planifiee.id
                for item in response_planifiees.data
            )
        )

        self.assertFalse(
            any(
                item["id"] == self.realisee.id
                for item in response_realisees.data
            )
        )

    def test_agronome_ne_peut_pas_consulter_detail_historique(self):
        self.client.force_authenticate(user=self.agronome)

        response_planifiee = self.client.get(
            f"/api/activites/{self.planifiee.id}/"
        )

        response_realisee = self.client.get(
            f"/api/activites/realisees/{self.realisee.id}/"
        )

        self.assertEqual(response_planifiee.status_code, 404)
        self.assertEqual(response_realisee.status_code, 404)
