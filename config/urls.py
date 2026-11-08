from django.contrib import admin
from django.urls import include, path

# HUIOS_HEALTH_CHECK_V1 — verifica aplicacao e conexao com o banco sem expor dados.
from django.db import connection
from django.http import JsonResponse


def healthcheck(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "down"}, status=503)
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", healthcheck, name="healthcheck"),
    path("admin/", admin.site.urls),
    path("", include("ct.urls")),
]
