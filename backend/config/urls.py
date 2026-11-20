from django.contrib import admin
from django.urls import include, path

from utilisateurs.views import ConnexionEmailAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # API utilisateurs
    path("api/utilisateurs/", include("utilisateurs.urls")),

    # Authentification JWT
    path(
        "api/token/",
        ConnexionEmailAPIView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path("api/parcelles/", include("parcelles.urls")),

        # API collaborations
    path("api/collaborations/", include("collaborations.urls")),

    # API notifications
    path("api/notifications/", include("notifications.urls")),
]