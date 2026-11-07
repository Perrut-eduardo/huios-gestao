# HUIOS GESTÃO — Projeto Social Huios BJJ

MVP acadêmico de apoio à gestão de necessidades, melhorias, campanhas e prestações de contas do centro de treinamento. Complementa o BJJ Control; **não substitui o controle de presença**.

## Tecnologias

Python 3.12, Django 5.2 LTS, SQLite, HTML5 e CSS responsivo.

## Executar localmente

No terminal, dentro do repositório:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py criar_perfis
python manage.py createsuperuser
python manage.py runserver
```

Se `py -3.12` não estiver disponível, instale o Python 3.12 e adapte o comando. Depois de criar um superusuário, atribua o grupo **Coordenacao** a ele pelo admin (ou use a conta superusuária para administrar). A aplicação estará em http://127.0.0.1:8000/ .

> Durante o desenvolvimento, use apenas informações fictícias. **Não publique** `db.sqlite3`, `.env`, chaves, senhas nem dados pessoais de alunos. O servidor `runserver` não serve para produção.

## Requisitos acadêmicos

- RF01: cadastrar necessidades; RF02: listar e filtrar; RF03: atualizar situação.
- RF04: registrar campanhas; RF05: registrar movimentações manuais; RF06: resumo financeiro.
- RNF01/RNF02: autenticação, validação, autorização por operação e ORM.
- RNF03: app responsivo e testável; RNF04: rótulos, estados textuais, foco e controles amplos.

## Histórico e CI

As etapas seguintes adicionam modelos, formulários, testes e GitHub Actions. Nenhuma integração bancária, WhatsApp automático ou integração com BJJ Control faz parte do MVP.
