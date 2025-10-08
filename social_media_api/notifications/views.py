# backend/notifications/views.py

from django.http import JsonResponse
from django.views import View

class NotificationListView(View):
    def get(self, request):
        return JsonResponse({"message": "Notifications endpoint working"})
