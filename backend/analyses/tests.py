
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

from .models import (
    ObservationNDVI,
    DonneeMeteo,
    AlerteAgricole,
    ConseilAgricole,
)


class AnalysesHistoriqueTests(APITestCase):

    def setUp(self):
        self.agriculteur = Utilisateur.objects.create_user(
            username="agriculteur_analyses",
            password="test123",
            role=Utilisateur.Role.AGRICULTEUR,
        )

        self.autre_agriculteur = Utilisateur.objects.create_user(
            username="autre_agriculteur",
            password="test123",
            role=Utilisateur.Role.AGRICULTEUR,
        )

        self.agronome = Utilisateur.objects.create_user(
            username="agronome_analyses",
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
            nom_parcelle="Parcelle test analyses",
            geometrie=geometrie,
            proprietaire=self.agriculteur,
        )

        maintenant = timezone.now()

        self.ndvi = ObservationNDVI.objects.create(
            parcelle=self.parcelle,
            valeur_ndvi=0.7500,
            date_acquisition_image=maintenant,
            date_traitement=maintenant,
            couverture_nuageuse=10.00,
            source_image="Sentinel-2",
            qualite_donnees="Bonne qualité",
        )

        self.meteo = DonneeMeteo.objects.create(
            parcelle=self.parcelle,
            date_meteo=maintenant,
            temperature=25.50,
            precipitation=2.50,
            humidite=70.00,
            source_meteo="Open-Meteo",
            date_recuperation=maintenant,
        )

        self.alerte = AlerteAgricole.objects.create(
            parcelle=self.parcelle,
            type_alerte="VEGETATION",
            niveau_alerte="MOYEN",
            contenu_alerte="Anomalie détectée.",
            date_alerte=maintenant,
        )

        self.conseil = ConseilAgricole.objects.create(
            parcelle=self.parcelle,
            contenu_conseil="Surveiller l'évolution de la culture.",
            source_conseil="IA",
            date_generation=maintenant,
        )

        # Suppression logique de la parcelle.
        Parcelle.objects.filter(pk=self.parcelle.pk).update(
            date_suppression=maintenant
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

        self.endpoints = [
            ("/api/analyses/ndvi/", self.ndvi),
            ("/api/analyses/meteo/", self.meteo),
            ("/api/analyses/alertes/", self.alerte),
            ("/api/analyses/conseils/", self.conseil),
        ]

    def test_agriculteur_peut_consulter_tout_historique(self):
        self.client.force_authenticate(user=self.agriculteur)

        for url, objet in self.endpoints:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

            self.assertTrue(
                any(
                    item["id"] == objet.id
                    for item in response.data
                )
            )

    def test_agriculteur_peut_consulter_details_historiques(self):
        self.client.force_authenticate(user=self.agriculteur)

        for url, objet in self.endpoints:
            detail_url = f"{url}{objet.id}/"
            response = self.client.get(detail_url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["id"], objet.id)

    def test_autre_agriculteur_ne_peut_pas_consulter_donnees(self):
        self.client.force_authenticate(user=self.autre_agriculteur)

        for url, objet in self.endpoints:
            response_liste = self.client.get(url)
            response_detail = self.client.get(f"{url}{objet.id}/")

            self.assertEqual(response_liste.status_code, 200)
            self.assertFalse(
                any(
                    item["id"] == objet.id
                    for item in response_liste.data
                )
            )
            self.assertEqual(response_detail.status_code, 404)

    def test_agronome_ne_peut_pas_consulter_historique_supprime(self):
        self.client.force_authenticate(user=self.agronome)

        for url, objet in self.endpoints:
            response_liste = self.client.get(url)
            response_detail = self.client.get(f"{url}{objet.id}/")

            self.assertEqual(response_liste.status_code, 200)
            self.assertFalse(
                any(
                    item["id"] == objet.id
                    for item in response_liste.data
                )
            )
            self.assertEqual(response_detail.status_code, 404)

    def test_api_est_strictement_en_lecture_seule(self):
        self.client.force_authenticate(user=self.agriculteur)

        for url, objet in self.endpoints:
            detail_url = f"{url}{objet.id}/"

            response_post = self.client.post(
                url,
                {},
                format="json",
            )

            response_put = self.client.put(
                detail_url,
                {},
                format="json",
            )

            response_patch = self.client.patch(
                detail_url,
                {},
                format="json",
            )

            response_delete = self.client.delete(detail_url)

            self.assertEqual(response_post.status_code, 405)
            self.assertEqual(response_put.status_code, 405)
            self.assertEqual(response_patch.status_code, 405)
            self.assertEqual(response_delete.status_code, 405)

        self.assertTrue(
            ObservationNDVI.objects.filter(pk=self.ndvi.pk).exists()
        )
        self.assertTrue(
            DonneeMeteo.objects.filter(pk=self.meteo.pk).exists()
        )
        self.assertTrue(
            AlerteAgricole.objects.filter(pk=self.alerte.pk).exists()
        )
        self.assertTrue(
            ConseilAgricole.objects.filter(pk=self.conseil.pk).exists()
        )
