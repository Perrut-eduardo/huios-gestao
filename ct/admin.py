from django.contrib import admin
from .models import Campanha, MovimentacaoFinanceira, Necessidade


@admin.register(Necessidade)
class NecessidadeAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "prioridade", "situacao", "responsavel", "criada_em")
    list_filter = ("situacao", "prioridade", "categoria")
    search_fields = ("titulo", "descricao")


@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "situacao", "data_inicio", "data_fim")
    list_filter = ("situacao",)


@admin.register(MovimentacaoFinanceira)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "tipo", "valor_centavos", "data_movimentacao")
    list_filter = ("tipo",)
