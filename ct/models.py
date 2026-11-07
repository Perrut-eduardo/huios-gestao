"""Dados do centro de treinamento. Valores monetários são armazenados em centavos."""
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Necessidade(models.Model):
    class Categoria(models.TextChoices):
        MATERIAL = "MATERIAL", "Material"
        MANUTENCAO = "MANUTENCAO", "Manutenção"
        MELHORIA = "MELHORIA", "Melhoria"

    class Prioridade(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Média"
        ALTA = "ALTA", "Alta"

    class Situacao(models.TextChoices):
        ABERTA = "ABERTA", "Aberta"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
        CONCLUIDA = "CONCLUIDA", "Concluída"

    titulo = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=15, choices=Categoria.choices)
    prioridade = models.CharField(max_length=5, choices=Prioridade.choices, default=Prioridade.MEDIA)
    situacao = models.CharField(max_length=15, choices=Situacao.choices, default=Situacao.ABERTA)
    custo_estimado_centavos = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    prazo_previsto = models.DateField(null=True, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="necessidades_criadas")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="necessidades_atribuidas")

    class Meta:
        ordering = ["-criada_em", "-id"]
        indexes = [models.Index(fields=["situacao", "prioridade"], name="ct_necessidade_sit_pri_idx")]

    def __str__(self):
        return self.titulo


class Campanha(models.Model):
    class Situacao(models.TextChoices):
        PLANEJADA = "PLANEJADA", "Planejada"
        ATIVA = "ATIVA", "Ativa"
        ENCERRADA = "ENCERRADA", "Encerrada"

    titulo = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    objetivo_centavos = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    situacao = models.CharField(max_length=10, choices=Situacao.choices, default=Situacao.PLANEJADA)
    necessidade = models.ForeignKey(Necessidade, on_delete=models.SET_NULL, blank=True, null=True, related_name="campanhas")
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="campanhas_criadas")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em", "-id"]

    def __str__(self):
        return self.titulo


class MovimentacaoFinanceira(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SAIDA = "SAIDA", "Saída"

    tipo = models.CharField(max_length=7, choices=Tipo.choices)
    descricao = models.CharField(max_length=180)
    valor_centavos = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    data_movimentacao = models.DateField()
    campanha = models.ForeignKey(Campanha, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimentacoes")
    necessidade = models.ForeignKey(Necessidade, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimentacoes")
    registrada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="movimentacoes_registradas")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_movimentacao", "-id"]

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.descricao}"
