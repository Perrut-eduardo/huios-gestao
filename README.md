# HUIOS GESTÃO — Projeto Social Huios BJJ

MVP acadêmico de apoio à gestão de necessidades, melhorias, campanhas e prestações de contas do centro de treinamento. **Complementa** o BJJ Control e não substitui o controle de presenças.

## Tecnologias e escopo

Python **3.12**, Django **5.2 LTS**, SQLite, HTML5 e CSS responsivo. Entidades: `Necessidade`, `Campanha`, `MovimentacaoFinanceira`, com usuários e grupos nativos do Django. Valores monetários são gravados como **inteiros em centavos**.

- RF01: cadastrar necessidades; RF02: listar e filtrar; RF03: atualizar situação.
- RF04: cadastrar campanhas; RF05: registrar movimentações manuais; RF06: exibir resumo financeiro.
- RNF01/RNF02: autenticação, permissões por operação, validação no servidor, proteção CSRF, ORM e escape de HTML.
- RNF03/RNF04: interface responsiva, controles amplos, rótulos persistentes e estados em texto.

## Como executar no Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py criar_perfis
python manage.py createsuperuser
python manage.py runserver
```

Acesse http://127.0.0.1:8000/ . Depois de criar o superusuário, atribua uma conta de teste ao grupo **Coordenacao** ou **Professor** em http://127.0.0.1:8000/admin/ . A conta superusuária pode administrar os cadastros.

> Se o comando de ativação do ambiente virtual for bloqueado pelo PowerShell, utilize ` .venv\Scripts\python.exe ` nos comandos seguintes, em vez de alterar políticas de segurança.

## Como executar os testes

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test --verbosity=2
```

O workflow de GitHub Actions (`.github/workflows/testes.yml`) executa essas verificações em `push` e `pull_request`. Consulte a aba **Actions** para confirmar o resultado real. O cadastro usa o banco SQLite local e não envia dados para serviços externos.

## Segurança e limitações

- Não publicar `db.sqlite3`, `.env`, chaves, senhas ou dados de alunos.
- Produção exige `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, HTTPS, armazenamento persistente, backups e servidor próprio para Django.
- O servidor `runserver` é exclusivo para desenvolvimento. Não há funcionamento offline.
- **Ainda não implementado:** limitação de tentativas de login, CSP de produção, backup/restore automatizado, métricas formais de desempenho e validação presencial com João Porto. Esses controles devem ser concluídos e testados antes de qualquer uso com dados reais.
- Não existe integração com BJJ Control, banco, Pix, WhatsApp automático nem aplicativo nativo.

## Etapas de versionamento para a Experiência Prática III

1. `chore: configurar estrutura inicial Django`
2. `feat: modelar necessidades campanhas e movimentacoes`
3. `feat: implementar fluxo de necessidades e financeiro`
4. `test: adicionar testes Django e integracao continua`

**Commits e resultados de testes só podem ser declarados como concluídos depois de executados e publicados.**
