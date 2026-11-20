from django.contrib import admin
from .models import (
    ObservationNDVI,
    DonneeMeteo,
    AlerteAgricole,
    ConseilAgricole
)

admin.site.register(ObservationNDVI)
admin.site.register(DonneeMeteo)
admin.site.register(AlerteAgricole)
admin.site.register(ConseilAgricole)