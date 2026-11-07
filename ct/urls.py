from django.http import HttpResponse
from django.urls import path


def inicio(request):
    return HttpResponse("HUIOS GESTÃO — estrutura Django iniciada.")


urlpatterns = [path("", inicio, name="painel")]
