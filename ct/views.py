"""Views: permissões verificadas no servidor, nunca somente por botões ocultos."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CampanhaForm, MovimentacaoForm, NecessidadeForm
from .models import Campanha, MovimentacaoFinanceira, Necessidade


@login_required
def painel(request):
    itens = Necessidade.objects.select_related("responsavel")
    situacao = request.GET.get("situacao", "")
    situacoes = dict(Necessidade.Situacao.choices)
    if situacao in situacoes:
        itens = itens.filter(situacao=situacao)
    else:
        situacao = ""
    totais = {s: Necessidade.objects.filter(situacao=s).count() for s in situacoes}
    return render(request, "ct/painel.html", {
        "necessidades": itens[:50], "totais": totais,
        "abertas": totais["ABERTA"], "andamento": totais["EM_ANDAMENTO"],
        "concluidas": totais["CONCLUIDA"], "situacao_ativa": situacao,
    })


@login_required
@permission_required("ct.add_necessidade", raise_exception=True)
def necessidade_nova(request):
    if request.method == "POST":
        form = NecessidadeForm(request.POST)
        if form.is_valid():
            necessidade = form.save(commit=False)
            necessidade.criada_por = request.user
            necessidade.situacao = Necessidade.Situacao.ABERTA
            necessidade.save()
            messages.success(request, "Necessidade cadastrada com sucesso!")
            return redirect("necessidade_detalhe", pk=necessidade.pk)
    else:
        form = NecessidadeForm()
    return render(request, "ct/formulario.html", {"form": form, "titulo": "Nova necessidade", "legenda": "Cadastre um material, manutenção ou melhoria do CT."})


@login_required
def necessidade_detalhe(request, pk):
    necessidade = get_object_or_404(Necessidade.objects.select_related("responsavel"), pk=pk)
    return render(request, "ct/detalhe.html", {"necessidade": necessidade})


@login_required
@permission_required("ct.change_necessidade", raise_exception=True)
@require_POST
def necessidade_situacao(request, pk):
    necessidade = get_object_or_404(Necessidade, pk=pk)
    situacao = request.POST.get("situacao", "")
    if situacao not in Necessidade.Situacao.values:
        return HttpResponseBadRequest("Selecione uma situação válida.")
    necessidade.situacao = situacao
    necessidade.save(update_fields=["situacao"])
    messages.success(request, "Situação atualizada.")
    return redirect("necessidade_detalhe", pk=pk)


@login_required
@permission_required("ct.view_campanha", raise_exception=True)
def campanhas(request):
    return render(request, "ct/campanhas.html", {"campanhas": Campanha.objects.select_related("necessidade")[:50]})


@login_required
@permission_required("ct.add_campanha", raise_exception=True)
def campanha_nova(request):
    form = CampanhaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        campanha = form.save(commit=False)
        campanha.criada_por = request.user
        campanha.save()
        messages.success(request, "Campanha registrada.")
        return redirect("campanhas")
    return render(request, "ct/formulario.html", {"form": form, "titulo": "Nova campanha", "legenda": "Associe uma campanha a uma necessidade, quando pertinente."})


@login_required
@permission_required("ct.add_movimentacaofinanceira", raise_exception=True)
def movimentacao_nova(request):
    form = MovimentacaoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        movimento = form.save(commit=False)
        movimento.registrada_por = request.user
        movimento.save()
        messages.success(request, "Movimentação registrada.")
        return redirect("resumo_financeiro")
    return render(request, "ct/formulario.html", {"form": form, "titulo": "Registrar entrada ou saída", "legenda": "Registros manuais, sem processamento de pagamentos."})


@login_required
@permission_required("ct.view_movimentacaofinanceira", raise_exception=True)
def resumo_financeiro(request):
    movimentos = MovimentacaoFinanceira.objects.select_related("campanha", "necessidade")
    inicio, fim = request.GET.get("inicio", ""), request.GET.get("fim", "")
    from datetime import date
    try:
        if inicio:
            inicio_data = date.fromisoformat(inicio)
            movimentos = movimentos.filter(data_movimentacao__gte=inicio_data)
        if fim:
            fim_data = date.fromisoformat(fim)
            movimentos = movimentos.filter(data_movimentacao__lte=fim_data)
    except ValueError:
        messages.error(request, "Informe datas válidas (AAAA-MM-DD).")
        return redirect("resumo_financeiro")
    entradas = movimentos.filter(tipo="ENTRADA").aggregate(s=Sum("valor_centavos"))["s"] or 0
    saidas = movimentos.filter(tipo="SAIDA").aggregate(s=Sum("valor_centavos"))["s"] or 0
    return render(request, "ct/financeiro.html", {
        "movimentos": movimentos[:50], "entradas": entradas, "saidas": saidas,
        "saldo": entradas - saidas, "inicio": inicio, "fim": fim,
    })
