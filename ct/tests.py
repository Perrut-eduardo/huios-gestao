"""Testes automatizados dos fluxos e controles essenciais do MVP."""
from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Campanha, MovimentacaoFinanceira, Necessidade


class FluxoMVPTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("criar_perfis", verbosity=0)
        usuario = get_user_model()
        cls.coord = usuario.objects.create_user(username="coordenacao_teste", password="SenhaSeguraTeste#2026")
        cls.prof = usuario.objects.create_user(username="professor_teste", password="SenhaSeguraTeste#2026")
        cls.coord.groups.add(Group.objects.get(name="Coordenacao"))
        cls.prof.groups.add(Group.objects.get(name="Professor"))

    @staticmethod
    def payload_necessidade(**changes):
        data = {"titulo": "Reposição de tatame", "descricao": "Troca de placas danificadas",
                "categoria": "MATERIAL", "prioridade": "ALTA", "custo_estimado": "500.00", "responsavel": "", "prazo_previsto": ""}
        data.update(changes)
        return data

    def criar_necessidade(self, **changes):
        return Necessidade.objects.create(
            titulo=changes.pop("titulo", "Reposição de tatame"),
            categoria=changes.pop("categoria", "MATERIAL"),
            prioridade=changes.pop("prioridade", "ALTA"),
            criada_por=self.coord, **changes,
        )

    def test_painel_exige_login(self):
        resposta = self.client.get(reverse("painel"))
        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login/", resposta.url)

    def test_professor_pode_consultar_mas_nao_cadastrar(self):
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get(reverse("painel")).status_code, 200)
        self.assertEqual(self.client.get(reverse("necessidade_nova")).status_code, 403)
        self.assertEqual(self.client.post(reverse("necessidade_nova"), self.payload_necessidade()).status_code, 403)
        self.assertFalse(Necessidade.objects.exists())

    def test_coord_cadastra_necessidade_com_valor_em_centavos(self):
        self.client.force_login(self.coord)
        resposta = self.client.post(reverse("necessidade_nova"), self.payload_necessidade(custo_estimado="500.10"))
        self.assertEqual(resposta.status_code, 302)
        item = Necessidade.objects.get()
        self.assertEqual(item.custo_estimado_centavos, 50010)
        self.assertEqual(item.situacao, "ABERTA")
        self.assertEqual(item.criada_por, self.coord)
        self.assertEqual(resposta.url, reverse("necessidade_detalhe", kwargs={"pk": item.pk}))

    def test_titulo_obrigatorio_rejeitado_no_servidor(self):
        self.client.force_login(self.coord)
        resposta = self.client.post(reverse("necessidade_nova"), self.payload_necessidade(titulo=""))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Este campo é obrigatório")
        self.assertEqual(Necessidade.objects.count(), 0)

    def test_custo_negativo_rejeitado(self):
        self.client.force_login(self.coord)
        resposta = self.client.post(reverse("necessidade_nova"), self.payload_necessidade(custo_estimado="-1"))
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Necessidade.objects.count(), 0)

    def test_texto_html_e_escapado_na_listagem(self):
        self.criar_necessidade(titulo="<script>alert(1)</script>")
        self.client.force_login(self.prof)
        resposta = self.client.get(reverse("painel"))
        self.assertContains(resposta, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(resposta, "<script>alert(1)</script>")

    def test_filtro_por_situacao(self):
        self.criar_necessidade(titulo="Aberta")
        self.criar_necessidade(titulo="Reforma do piso finalizada", situacao="CONCLUIDA")
        self.client.force_login(self.prof)
        resposta = self.client.get(reverse("painel"), {"situacao": "ABERTA"})
        self.assertContains(resposta, "Aberta")
        self.assertNotContains(resposta, "Reforma do piso finalizada")

    def test_alteracao_de_situacao_exige_post(self):
        item = self.criar_necessidade()
        self.client.force_login(self.coord)
        self.assertEqual(self.client.get(reverse("necessidade_situacao", args=[item.pk])).status_code, 405)
        item.refresh_from_db()
        self.assertEqual(item.situacao, "ABERTA")

    def test_coord_pode_atualizar_situacao(self):
        item = self.criar_necessidade()
        self.client.force_login(self.coord)
        resposta = self.client.post(reverse("necessidade_situacao", args=[item.pk]), {"situacao": "CONCLUIDA"})
        self.assertEqual(resposta.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.situacao, "CONCLUIDA")

    def test_professor_nao_altera_situacao(self):
        item = self.criar_necessidade()
        self.client.force_login(self.prof)
        resposta = self.client.post(reverse("necessidade_situacao", args=[item.pk]), {"situacao": "CONCLUIDA"})
        self.assertEqual(resposta.status_code, 403)
        item.refresh_from_db()
        self.assertEqual(item.situacao, "ABERTA")

    def test_campanha_criada_com_vinculo(self):
        item = self.criar_necessidade()
        self.client.force_login(self.coord)
        resposta = self.client.post(reverse("campanha_nova"), {
            "titulo": "Campanha de tatame", "descricao": "Apoio fictício", "objetivo": "100.00",
            "data_inicio": "2026-11-06", "data_fim": "2026-12-06", "situacao": "ATIVA", "necessidade": item.pk,
        })
        self.assertEqual(resposta.status_code, 302)
        campanha = Campanha.objects.get()
        self.assertEqual(campanha.objetivo_centavos, 10000)
        self.assertEqual(campanha.necessidade, item)

    def test_campanha_rejeita_datas_invertidas(self):
        self.client.force_login(self.coord)
        resposta = self.client.post(reverse("campanha_nova"), {
            "titulo": "Campanha", "data_inicio": "2026-12-06", "data_fim": "2026-11-06", "situacao": "ATIVA",
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Campanha.objects.exists())

    def test_resumo_financeiro_sem_contagem_duplicada(self):
        item = self.criar_necessidade()
        campanha = Campanha.objects.create(titulo="Campanha fictícia", data_inicio=date(2026, 11, 6),
                                           criada_por=self.coord, necessidade=item)
        self.client.force_login(self.coord)
        for tipo, valor in (("ENTRADA", "200.00"), ("SAIDA", "80.00")):
            resposta = self.client.post(reverse("movimentacao_nova"), {
                "tipo": tipo, "descricao": "Registro fictício", "valor": valor,
                "data_movimentacao": "2026-11-06", "campanha": campanha.pk, "necessidade": item.pk,
            })
            self.assertEqual(resposta.status_code, 302)
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 2)
        resposta = self.client.get(reverse("resumo_financeiro"))
        self.assertContains(resposta, "R$ 200,00")
        self.assertContains(resposta, "R$ 80,00")
        self.assertContains(resposta, "R$ 120,00")

    def test_professor_nao_acessa_movimentacoes(self):
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get(reverse("resumo_financeiro")).status_code, 403)
        self.assertEqual(self.client.post(reverse("movimentacao_nova"), {}).status_code, 403)
        self.assertFalse(MovimentacaoFinanceira.objects.exists())
