
from django.contrib import admin
from .models import (
    CandidatureAgronome,
    DocumentCandidature,
    DemandeRecommandation,
    AutorisationAcces,
    RecommandationAgricole
)

admin.site.register(CandidatureAgronome)
admin.site.register(DocumentCandidature)
admin.site.register(DemandeRecommandation)
admin.site.register(AutorisationAcces)
admin.site.register(RecommandationAgricole)
