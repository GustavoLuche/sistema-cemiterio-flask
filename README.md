# Sistema de Busca de Túmulos - Cemitério da Igualdade

Aplicação web desenvolvida no Projeto Integrador (UNIVESP) para localizar registros de falecidos no Cemitério da Igualdade.

## Funcionalidades

### Busca pública
- Filtros por nome, lápide (jazigo), setor, quadra e intervalo de data de falecimento.
- Resultado em cards com dados de localização (setor, quadra e jazigo).
- Layout responsivo para desktop e mobile.

### Painel administrativo
- Login obrigatório com sessão.
- Cadastro de novos registros.
- Listagem com paginação.
- Busca de registros por nome, setor e quadra.
- Edição de registros existentes.
- Loading visual durante busca/listagem.

## Tecnologias

- Python 3.12+
- Flask 3
- PostgreSQL
- psycopg 3
- Gunicorn
- HTML, CSS e JavaScript (vanilla)

## Estrutura principal

```text
app.py
schema.sql
seed_data.py
requirements.txt
render.yaml
templates/
    base.html
    index.html
    admin.html
    admin_login.html
static/
    styles.css
docs/
```

## Configuração local

### 1. Ambiente virtual e dependências

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Variáveis de ambiente

Crie o arquivo `.env` (baseado no `.env.example`) com os valores mínimos:

```env
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
FLASK_SECRET_KEY=troque-por-uma-chave-segura

# Usuario admin inicial (criado automaticamente no banco se nao existir)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_EMAIL=admin@admin.local

FLASK_DEBUG=True
PORT=5000
```

### 3. Inicialização do banco

Ao subir a aplicação, o `app.py` executa migração/ajustes automaticamente:
- cria tabela `falecidos` (se não existir)
- cria tabela `usuarios` (autenticação admin)
- garante índices
- cria usuário admin inicial se ainda não existir

Opcionalmente, você pode aplicar o schema manualmente:

```bash
psql -U seu_usuario -d seu_banco -f schema.sql
```

### 4. Executar aplicação

```bash
python app.py
```

Acesse:
- Busca pública: `http://localhost:5000/`
- Login admin: `http://localhost:5000/admin/login`

## Seed de dados

Para popular com dados fictícios de teste:

```bash
python seed_data.py
```

## Endpoints principais

### Público
- `GET /`
- `POST /api/buscar`
- `GET /api/filtros`

### Administrativo (protegido por sessão)
- `GET /admin`
- `GET /admin/login`
- `POST /admin/login`
- `POST /admin/logout`
- `GET /api/admin/registros`
- `POST /api/admin/adicionar`
- `PUT /api/admin/editar/<id>`
- `DELETE /api/admin/deletar/<id>`

## Deploy no Render

O projeto já possui `render.yaml` com blueprint para:
- banco PostgreSQL
- web service Flask com Gunicorn

Passos:
1. No Render, criar via Blueprint usando o repositório.
2. Confirmar variáveis de ambiente (principalmente `DATABASE_URL`, `FLASK_SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `ADMIN_EMAIL`).
3. Publicar.

## Segurança (recomendado)

- Defina `FLASK_SECRET_KEY` forte em produção.
- Troque `ADMIN_PASSWORD` padrão antes de publicar.
- Use HTTPS no ambiente de produção.

## Contexto acadêmico

Projeto educacional desenvolvido pelo Grupo 3 - UNIVESP, no âmbito do Projeto Integrador.
