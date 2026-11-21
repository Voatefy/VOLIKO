from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APITestCase

from utilisateurs.models import Utilisateur
from .models import (
    Notification,
    PreferenceNotification,
    TypeNotification,
    CanalNotification,
)
from .services import (
    envoyer_notification_application,
    envoyer_notification_email,
)


class NotificationAPITests(APITestCase):

    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            username="utilisateur_notifications",
            password="test123",
            email="user@test.com",
        )

        self.autre_utilisateur = Utilisateur.objects.create_user(
            username="autre_notifications",
            password="test123",
            email="autre@test.com",
        )

        self.notification = Notification.objects.create(
            destinataire=self.utilisateur,
            contenu="Une nouvelle alerte agricole.",
            type_notification=TypeNotification.ALERTE,
        )

        self.autre_notification = Notification.objects.create(
            destinataire=self.autre_utilisateur,
            contenu="Notification privée.",
            type_notification=TypeNotification.ACTIVITE,
        )

        self.client.force_authenticate(user=self.utilisateur)

    def test_utilisateur_consulte_uniquement_ses_notifications(self):
        response = self.client.get("/api/notifications/")

        self.assertEqual(response.status_code, 200)

        ids = [item["id"] for item in response.data]

        self.assertIn(self.notification.id, ids)
        self.assertNotIn(self.autre_notification.id, ids)

    def test_utilisateur_ne_peut_pas_consulter_notification_autrui(self):
        response = self.client.get(
            f"/api/notifications/{self.autre_notification.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_utilisateur_peut_consulter_une_notification(self):
        response = self.client.get(
            f"/api/notifications/{self.notification.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.notification.id)

    def test_utilisateur_peut_marquer_notification_comme_lue(self):
        response = self.client.patch(
            f"/api/notifications/{self.notification.id}/lue/"
        )

        self.assertEqual(response.status_code, 200)

        self.notification.refresh_from_db()
        self.assertIsNotNone(self.notification.date_lecture)

    def test_utilisateur_ne_peut_pas_marquer_notification_autrui_comme_lue(self):
        response = self.client.patch(
            f"/api/notifications/{self.autre_notification.id}/lue/"
        )

        self.assertEqual(response.status_code, 404)

    def test_api_ne_permet_pas_de_modifier_notification(self):
        url = f"/api/notifications/{self.notification.id}/"

        response_put = self.client.put(url, {}, format="json")
        response_patch = self.client.patch(url, {}, format="json")
        response_delete = self.client.delete(url)

        self.assertEqual(response_put.status_code, 405)
        self.assertEqual(response_patch.status_code, 405)
        self.assertEqual(response_delete.status_code, 405)

    def test_utilisateur_ne_peut_pas_creer_notification_directement(self):
        response = self.client.post(
            "/api/notifications/",
            {
                "contenu": "Notification frauduleuse.",
                "type_notification": TypeNotification.ALERTE,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 405)

    def test_utilisateur_peut_creer_sa_preference(self):
        response = self.client.post(
            "/api/notifications/preferences/",
            {
                "categorie_notification": TypeNotification.ALERTE,
                "canal": CanalNotification.EMAIL,
                "est_active": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            PreferenceNotification.objects.filter(
                utilisateur=self.utilisateur,
                categorie_notification=TypeNotification.ALERTE,
                canal=CanalNotification.EMAIL,
                est_active=False,
            ).exists()
        )

    def test_utilisateur_ne_peut_pas_creer_preference_en_double(self):
        PreferenceNotification.objects.create(
            utilisateur=self.utilisateur,
            categorie_notification=TypeNotification.ALERTE,
            canal=CanalNotification.EMAIL,
        )

        response = self.client.post(
            "/api/notifications/preferences/",
            {
                "categorie_notification": TypeNotification.ALERTE,
                "canal": CanalNotification.EMAIL,
                "est_active": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_utilisateur_ne_consulte_que_ses_preferences(self):
        autre_preference = PreferenceNotification.objects.create(
            utilisateur=self.autre_utilisateur,
            categorie_notification=TypeNotification.ALERTE,
            canal=CanalNotification.EMAIL,
        )

        response = self.client.get(
            "/api/notifications/preferences/"
        )

        self.assertEqual(response.status_code, 200)

        ids = [item["id"] for item in response.data]
        self.assertNotIn(autre_preference.id, ids)

    def test_utilisateur_ne_peut_pas_modifier_preference_autrui(self):
        preference = PreferenceNotification.objects.create(
            utilisateur=self.autre_utilisateur,
            categorie_notification=TypeNotification.ALERTE,
            canal=CanalNotification.EMAIL,
        )

        response = self.client.patch(
            f"/api/notifications/preferences/{preference.id}/",
            {"est_active": False},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_utilisateur_ne_peut_pas_supprimer_preference_autrui(self):
        preference = PreferenceNotification.objects.create(
            utilisateur=self.autre_utilisateur,
            categorie_notification=TypeNotification.ALERTE,
            canal=CanalNotification.EMAIL,
        )

        response = self.client.delete(
            f"/api/notifications/preferences/{preference.id}/"
        )

        self.assertEqual(response.status_code, 404)


class NotificationServicesTests(TestCase):

    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            username="services_notifications",
            password="test123",
            email="services@test.com",
        )

    def test_notification_application_creee_sans_preference(self):
        notification = envoyer_notification_application(
            self.utilisateur,
            TypeNotification.ALERTE,
            "Nouvelle alerte.",
        )

        self.assertIsNotNone(notification)
        self.assertTrue(
            Notification.objects.filter(pk=notification.pk).exists()
        )

    def test_notification_application_desactivee(self):
        PreferenceNotification.objects.create(
            utilisateur=self.utilisateur,
            categorie_notification=TypeNotification.ALERTE,
            canal=CanalNotification.APPLICATION,
            est_active=False,
        )

        notification = envoyer_notification_application(
            self.utilisateur,
            TypeNotification.ALERTE,
            "Nouvelle alerte.",
        )

        self.assertIsNone(notification)
        self.assertFalse(
            Notification.objects.filter(
                destinataire=self.utilisateur
            ).exists()
        )

    @patch("notifications.services.send_mail")
    def test_email_envoye_sans_preference(self, mock_send_mail):
        resultat = envoyer_notification_email(
            self.utilisateur,
            TypeNotification.ALERTE,
            "Nouvelle alerte",
            "Une anomalie a été détectée.",
        )

        self.assertTrue(resultat)
        mock_send_mail.assert_called_once()

    @patch("notifications.services.send_mail")
    def test_email_non_envoye_si_preference_desactivee(self, mock_send_mail):
        PreferenceNotification.objects.create(
            utilisateur=self.utilisateur,
            categorie_notification=TypeNotification.ALERTE,
            canal=CanalNotification.EMAIL,
            est_active=False,
        )

        resultat = envoyer_notification_email(
            self.utilisateur,
            TypeNotification.ALERTE,
            "Nouvelle alerte",
            "Une anomalie a été détectée.",
        )

        self.assertFalse(resultat)
        mock_send_mail.assert_not_called()

    @patch("notifications.services.send_mail")
    def test_email_non_envoye_si_adresse_absente(self, mock_send_mail):
        self.utilisateur.email = ""
        self.utilisateur.save(update_fields=["email"])

        resultat = envoyer_notification_email(
            self.utilisateur,
            TypeNotification.ALERTE,
            "Nouvelle alerte",
            "Une anomalie a été détectée.",
        )

        self.assertFalse(resultat)
        mock_send_mail.assert_not_called()
