from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Notification, PreferenceNotification
from .serializers import (
    NotificationSerializer,
    PreferenceNotificationSerializer,
)


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            destinataire=self.request.user
        ).order_by("-date_creation")


class NotificationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            destinataire=self.request.user
        )


class NotificationMarquerLueAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        notification = get_object_or_404(
            Notification,
            pk=pk,
            destinataire=request.user
        )

        if notification.date_lecture is None:
            notification.date_lecture = timezone.now()
            notification.save(update_fields=["date_lecture"])

        return Response(
            NotificationSerializer(notification).data
        )

class PreferenceNotificationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PreferenceNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PreferenceNotification.objects.filter(
            utilisateur=self.request.user
        ).order_by("categorie_notification", "canal")

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)


class PreferenceNotificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PreferenceNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PreferenceNotification.objects.filter(
            utilisateur=self.request.user
        )