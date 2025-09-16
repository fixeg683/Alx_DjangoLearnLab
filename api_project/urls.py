from django.contrib import admin
from django.urls import path, include
from api.views import home  # <-- import home view

urlpatterns = [
    path("", home, name="home"),  # <-- root URL
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api-token-auth/", include("rest_framework.urls")),  # login/logout for browsable API
]
