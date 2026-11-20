from django.conf import settings
from django.core.mail import send_mail

from .models import (
    Notification,
    PreferenceNotification,
    CanalNotification,
)


def envoyer_notification_application(
    destinataire,
    categorie,
    contenu,
):
    preference = PreferenceNotification.objects.filter(
        utilisateur=destinataire,
        categorie_notification=categorie,
        canal=CanalNotification.APPLICATION,
    ).first()

    if preference and not preference.est_active:
        return None

    return Notification.objects.create(
        destinataire=destinataire,
        type_notification=categorie,
        contenu=contenu,
    )


def envoyer_notification_email(
    destinataire,
    categorie,
    sujet,
    contenu,
):
    preference = PreferenceNotification.objects.filter(
        utilisateur=destinataire,
        categorie_notification=categorie,
        canal=CanalNotification.EMAIL,
    ).first()

    if preference and not preference.est_active:
        return False

    if not destinataire.email:
        return False

    send_mail(
        subject=sujet,
        message=contenu,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destinataire.email],
        fail_silently=False,
    )

    return True