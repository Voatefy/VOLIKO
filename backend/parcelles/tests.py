
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.utils import timezone

from rest_framework.test import APITestCase

from utilisateurs.models import Utilisateur
from parcelles.models import Parcelle, Culture, CultureParcelle
from collaborations.models import (
    AutorisationAcces,
    PorteeAcces,
    StatutDemandeAcces,
    StatutAutorisation,
)


class ParcellesHistoriqueTests(APITestCase):

    def setUp(self):
        self.agriculteur = Utilisateur.objects.create_user(
            username="agriculteur_test",
            password="test123",
            role=Utilisateur.Role.AGRICULTEUR,
        )

        self.autre_agriculteur = Utilisateur.objects.create_user(
            username="autre_agriculteur",
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

        self.parcelle = Parcelle.objects.create(
            nom_parcelle="Parcelle test",
            geometrie=MultiPolygon(polygon, srid=4326),
            proprietaire=self.agriculteur,
        )

        self.culture = Culture.objects.create(
            nom_culture="Riz",
        )

        self.association = CultureParcelle.objects.create(
            parcelle=self.parcelle,
            culture=self.culture,
            variete="Makalioka",
        )

        Parcelle.objects.filter(pk=self.parcelle.pk).update(
            date_suppression=timezone.now()
        )

        self.parcelle.refresh_from_db()

        AutorisationAcces.objects.create(
            agriculteur=self.agriculteur,
            agronome=self.agronome,
            portee=PorteeAcces.TOUTES,
            statut_demande=StatutDemandeAcces.ACCEPTEE,
            statut_autorisation=StatutAutorisation.ACTIVE,
        )

    def test_agriculteur_peut_consulter_culture_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        response = self.client.get("/api/parcelles/cultures/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(
                item["id"] == self.association.id
                for item in response.data
            )
        )

    def test_agriculteur_peut_consulter_detail_culture_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        response = self.client.get(
            f"/api/parcelles/cultures/{self.association.id}/"
        )

        self.assertEqual(response.status_code, 200)

    def test_agriculteur_ne_peut_pas_modifier_culture_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        response = self.client.patch(
            f"/api/parcelles/cultures/{self.association.id}/",
            {"variete": "Nouvelle variété"},
            format="json",
        )

        self.assertIn(response.status_code, [400, 403])

        self.association.refresh_from_db()
        self.assertEqual(self.association.variete, "Makalioka")

    def test_agriculteur_ne_peut_pas_supprimer_culture_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        response = self.client.delete(
            f"/api/parcelles/cultures/{self.association.id}/"
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            CultureParcelle.objects.filter(
                pk=self.association.id
            ).exists()
        )

    def test_agronome_ne_peut_pas_consulter_culture_historique(self):
        self.client.force_authenticate(user=self.agronome)

        response = self.client.get("/api/parcelles/cultures/")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            any(
                item["id"] == self.association.id
                for item in response.data
            )
        )

    def test_agronome_ne_peut_pas_consulter_detail_historique(self):
        self.client.force_authenticate(user=self.agronome)

        response = self.client.get(
            f"/api/parcelles/cultures/{self.association.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_autre_agriculteur_ne_peut_pas_consulter_historique(self):
        self.client.force_authenticate(user=self.autre_agriculteur)

        response = self.client.get("/api/parcelles/cultures/")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            any(
                item["id"] == self.association.id
                for item in response.data
            )
        )

    def test_creation_culture_sur_parcelle_supprimee_refusee(self):
        self.client.force_authenticate(user=self.agriculteur)

        response = self.client.post(
            "/api/parcelles/cultures/",
            {
                "parcelle": self.parcelle.id,
                "culture": self.culture.id,
                "variete": "Nouvelle variété",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
