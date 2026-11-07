"""Formulários com validação obrigatória no servidor."""
from decimal import Decimal
from django import forms
from .models import Campanha, MovimentacaoFinanceira, Necessidade


class NecessidadeForm(forms.ModelForm):
    custo_estimado = forms.DecimalField(
        label="Custo estimado (R$)", max_digits=11, decimal_places=2,
        min_value=Decimal("0.00"), required=False,
        help_text="Opcional. Informe um valor maior ou igual a zero.",
    )

    class Meta:
        model = Necessidade
        fields = ["titulo", "categoria", "prioridade", "descricao", "responsavel", "prazo_previsto"]
        labels = {"titulo": "Título da necessidade", "descricao": "Descrição complementar", "responsavel": "Responsável (opcional)"}
        widgets = {"descricao": forms.Textarea(attrs={"rows": 3}), "prazo_previsto": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.custo_estimado_centavos is not None:
            self.fields["custo_estimado"].initial = Decimal(self.instance.custo_estimado_centavos) / 100
        self.fields["responsavel"].required = False

    def save(self, commit=True):
        objeto = super().save(commit=False)
        custo = self.cleaned_data["custo_estimado"]
        objeto.custo_estimado_centavos = None if custo is None else int(custo * 100)
        if commit:
            objeto.save()
            self.save_m2m()
        return objeto


class CampanhaForm(forms.ModelForm):
    objetivo = forms.DecimalField(label="Objetivo de arrecadação (R$)", max_digits=11, decimal_places=2,
                                  min_value=Decimal("0.01"), required=False)

    class Meta:
        model = Campanha
        fields = ["titulo", "descricao", "data_inicio", "data_fim", "situacao", "necessidade"]
        widgets = {"descricao": forms.Textarea(attrs={"rows": 3}),
                   "data_inicio": forms.DateInput(attrs={"type": "date"}),
                   "data_fim": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        data = super().clean()
        if data.get("data_fim") and data.get("data_inicio") and data["data_fim"] < data["data_inicio"]:
            self.add_error("data_fim", "A data final não pode ser anterior à inicial.")
        return data

    def save(self, commit=True):
        objeto = super().save(commit=False)
        objetivo = self.cleaned_data["objetivo"]
        objeto.objetivo_centavos = None if objetivo is None else int(objetivo * 100)
        if commit:
            objeto.save()
            self.save_m2m()
        return objeto


class MovimentacaoForm(forms.ModelForm):
    valor = forms.DecimalField(label="Valor (R$)", max_digits=11, decimal_places=2,
                               min_value=Decimal("0.01"), required=True)

    class Meta:
        model = MovimentacaoFinanceira
        fields = ["tipo", "descricao", "data_movimentacao", "campanha", "necessidade"]
        widgets = {"data_movimentacao": forms.DateInput(attrs={"type": "date"})}

    def save(self, commit=True):
        objeto = super().save(commit=False)
        objeto.valor_centavos = int(self.cleaned_data["valor"] * 100)
        if commit:
            objeto.save()
            self.save_m2m()
        return objeto
