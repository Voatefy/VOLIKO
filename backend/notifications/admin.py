
from django.contrib import admin
from .models import Notification, PreferenceNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "destinataire",
        "type_notification",
        "date_creation",
        "date_lecture"
    )
    list_filter = ("type_notification", "date_creation")
    search_fields = ("destinataire__username", "contenu")


@admin.register(PreferenceNotification)
class PreferenceNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "utilisateur",
        "categorie_notification",
        "canal",
        "est_active"
    )
    list_filter = ("categorie_notification", "canal", "est_active")
    search_fields = ("utilisateur__username",)
