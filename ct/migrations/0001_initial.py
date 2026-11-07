# Migração inicial do projeto HUIOS GESTÃO.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Necessidade",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("titulo", models.CharField(max_length=120)),
                ("descricao", models.TextField(blank=True)),
                ("categoria", models.CharField(choices=[("MATERIAL", "Material"), ("MANUTENCAO", "Manutenção"), ("MELHORIA", "Melhoria")], max_length=15)),
                ("prioridade", models.CharField(choices=[("BAIXA", "Baixa"), ("MEDIA", "Média"), ("ALTA", "Alta")], default="MEDIA", max_length=5)),
                ("situacao", models.CharField(choices=[("ABERTA", "Aberta"), ("EM_ANDAMENTO", "Em andamento"), ("CONCLUIDA", "Concluída")], default="ABERTA", max_length=15)),
                ("custo_estimado_centavos", models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ("prazo_previsto", models.DateField(blank=True, null=True)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("criada_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="necessidades_criadas", to=settings.AUTH_USER_MODEL)),
                ("responsavel", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="necessidades_atribuidas", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-criada_em", "-id"]},
        ),
        migrations.AddIndex(model_name="necessidade", index=models.Index(fields=["situacao", "prioridade"], name="ct_necessidade_sit_pri_idx")),
        migrations.CreateModel(
            name="Campanha",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("titulo", models.CharField(max_length=120)),
                ("descricao", models.TextField(blank=True)),
                ("objetivo_centavos", models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ("data_inicio", models.DateField()),
                ("data_fim", models.DateField(blank=True, null=True)),
                ("situacao", models.CharField(choices=[("PLANEJADA", "Planejada"), ("ATIVA", "Ativa"), ("ENCERRADA", "Encerrada")], default="PLANEJADA", max_length=10)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("criada_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="campanhas_criadas", to=settings.AUTH_USER_MODEL)),
                ("necessidade", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="campanhas", to="ct.necessidade")),
            ],
            options={"ordering": ["-criada_em", "-id"]},
        ),
        migrations.CreateModel(
            name="MovimentacaoFinanceira",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("tipo", models.CharField(choices=[("ENTRADA", "Entrada"), ("SAIDA", "Saída")], max_length=7)),
                ("descricao", models.CharField(max_length=180)),
                ("valor_centavos", models.PositiveBigIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("data_movimentacao", models.DateField()),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("campanha", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="movimentacoes", to="ct.campanha")),
                ("necessidade", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="movimentacoes", to="ct.necessidade")),
                ("registrada_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="movimentacoes_registradas", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-data_movimentacao", "-id"]},
        ),
    ]
