from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.painel, name="painel"),
    path("necessidades/nova/", views.necessidade_nova, name="necessidade_nova"),
    path("necessidades/<int:pk>/", views.necessidade_detalhe, name="necessidade_detalhe"),
    path("necessidades/<int:pk>/situacao/", views.necessidade_situacao, name="necessidade_situacao"),
    path("campanhas/", views.campanhas, name="campanhas"),
    path("campanhas/nova/", views.campanha_nova, name="campanha_nova"),
    path("financeiro/", views.resumo_financeiro, name="resumo_financeiro"),
    path("financeiro/novo/", views.movimentacao_nova, name="movimentacao_nova"),
]
