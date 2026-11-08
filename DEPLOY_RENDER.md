# Deploy HUIOS GESTAO / Render — ambiente academico

Nao cadastre dados pessoais reais de alunos, responsaveis ou menores neste ambiente gratuito.

## Render Web Service (plano Free)
- Branch: main
- Runtime: Python 3
- Build Command: `bash build.sh`
- Start Command: `bash start.sh`
- Root Directory: vazio

## Environment Variables — Render (nao enviar ao GitHub)
- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` = string aleatoria forte, gerada no painel (nao compartilhar)
- `DATABASE_URL` = URL de um PostgreSQL persistente, por exemplo Neon; copiar para campo secreto
- `HUIOS_DEMO_USERNAME` = nome de usuario ficticio, escolhido pelo proprietario
- `HUIOS_DEMO_PASSWORD` = senha forte de 12+ caracteres, **nao compartilhar no chat**

As variaveis `RENDER` e `RENDER_EXTERNAL_HOSTNAME` sao disponibilizadas automaticamente pela plataforma.
O `HUIOS_DEMO_PASSWORD` pode ser retirado das variaveis de ambiente depois da primeira criacao, mantendo-se a conta no banco.

## Monitoramento
- Verificacao HTTP GET em `https://<dominio-do-servico>.onrender.com/health/`
- Resposta 200 `{"status":"ok"}` caso Django e PostgreSQL estejam funcionando
- Resposta 503 `{"status":"down"}` caso a consulta ao banco falhe
- Em instancias gratuitas, o primeiro acesso depois de inatividade pode demorar

## Cuidados
- Nao utilizar o SQLite do notebook em producao: o Render Free nao possui disco persistente.
- O script de startup aplica migracoes na base do PostgreSQL e sobe Gunicorn.
- Nunca registrar senhas ou URLs de banco em screenshots da DreamShaper.
- Antes de publicar, conferir o Pull Request de seguranca e migracoes pendentes.
