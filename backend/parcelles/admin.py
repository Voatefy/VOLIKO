from django.contrib import admin
from .models import Parcelle, Culture, CultureParcelle

admin.site.register(Parcelle)
admin.site.register(Culture)
admin.site.register(CultureParcelle)