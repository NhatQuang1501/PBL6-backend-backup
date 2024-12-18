from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("api/", include("application.urls")),
    path("api/", include("chat.urls")),
]
