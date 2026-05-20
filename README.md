# 🏛️ Sistema de Busca de Túmulos - Cemitério da Igualdade

**Grupo 3 - UNIVESP - Projeto Integrador (PI)**

## 📋 Sobre o Projeto

Sistema web para facilitar a busca de registros de falecidos no Cemitério da Igualdade, localizado em Primavera, Rosana-SP. Desenvolvido como resposta a um problema identificado através de Design Thinking: centenas de visitantes mensais têm dificuldade em localizar túmulos devido ao layout não sequencial do cemitério.

**Validação**: 29 pessoas responderam a pesquisa Microsoft Forms com 83-93% de apoio à solução digital.

## 🚀 Características MVP

- ✅ **Busca por Nome**: Busca case-insensitive de falecidos
- ✅ **Localização**: Exibição de setor, quadra e jazigo
- ✅ **Interface Responsiva**: Funciona em desktop, tablet e mobile
- ✅ **Painel Admin**: Criar, editar e deletar registros (futuro: com autenticação)
- ✅ **Validação**: Campos obrigatórios e feedback do usuário
- ✅ **API REST**: Endpoints para integração futura

## 🛠️ Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Backend | Flask | 3.0.0 |
| Banco de Dados | PostgreSQL | 12+ |
| Frontend | HTML5 + CSS3 | - |
| Linguagem | Python | 3.10+ |
| Hospedagem | Railway (prod) | - |

## 📦 Instalação Local

### Pré-requisitos
- Python 3.10+
- PostgreSQL 12+
- Git

### Passo 1: Clonar Repositório
```bash
git clone https://github.com/GustavoLuche/sistema-cemiterio-flask.git
cd sistema-cemiterio-flask
```

### Passo 2: Criar Ambiente Virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados
1. Criar arquivo `.env` baseado em `.env.example`
2. Adicionar `DATABASE_URL` com suas credenciais PostgreSQL
3. Executar schema:
```bash
psql -U seu_usuario -d seu_banco -f schema.sql
```

### Passo 5: Executar Aplicação
```bash
python app.py
```
Acesse em: http://localhost:5000

## 📚 Estrutura do Projeto

```
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── schema.sql            # Schema do banco de dados
├── .env.example          # Template de variáveis de ambiente
├── README.md             # Este arquivo
├── static/
│   └── styles.css        # Folha de estilos
└── templates/
    ├── base.html         # Template base
    ├── index.html        # Página de busca (público)
    └── admin.html        # Painel administrativo
```

## 🔌 API Endpoints

### Busca Pública
- **GET** `/` - Página inicial
- **POST** `/api/buscar` - Buscar falecido por nome

### Admin (Futuro com autenticação)
- **GET** `/admin` - Painel administrativo
- **GET** `/api/admin/registros` - Listar todos
- **POST** `/api/admin/adicionar` - Novo registro
- **PUT** `/api/admin/editar/<id>` - Editar registro
- **DELETE** `/api/admin/deletar/<id>` - Deletar registro

## 🗄️ Modelo de Dados

```sql
-- Tabela principal de falecidos
falecidos
├── id (PK)
├── nome_falecido (VARCHAR)
├── data_falecimento (DATE)
├── cemiterio (VARCHAR)
├── setor (VARCHAR)
├── quadra (VARCHAR)
├── jazigo (VARCHAR)
├── observacoes (TEXT)
├── data_criacao (TIMESTAMP)
└── data_atualizacao (TIMESTAMP)
```

## 🚢 Deploy no Railway

### 1. Criar Conta Railway
https://railway.app

### 2. Conectar GitHub
- Login com conta GitHub
- Autorizar Railway

### 3. Criar Projeto
- New Project → GitHub Repo
- Selecionar `sistema-cemiterio-flask`

### 4. Adicionar PostgreSQL
- Add Service → PostgreSQL
- Railway gera `DATABASE_URL` automaticamente

### 5. Configurar Variáveis de Ambiente
No dashboard Railway:
```
DATABASE_URL: (gerado automaticamente)
FLASK_ENV: production
FLASK_DEBUG: False
```

### 6. Deploy
Railway faz deploy automático ao fazer push para `main`

## 📱 Uso

### Buscar Falecido
1. Acesse a página inicial
2. Digite o nome (parcial ou completo)
3. Clique em "Buscar"
4. Resultado mostra setor/quadra/jazigo

### Admin (Futuro)
1. Acesse `/admin`
2. Autentique (será implementado)
3. Gerencie registros (criar, editar, deletar)

## 🧪 Testes (Futuro)

```bash
pytest tests/
```

## 🤝 Contribuindo

1. Crie uma branch: `git checkout -b feature/nova-feature`
2. Commit suas mudanças: `git commit -m 'Add nova feature'`
3. Push: `git push origin feature/nova-feature`
4. Abra Pull Request

## 📅 Timeline Projeto

- **Q2 (Fev-Mar)**: Planejamento e Design
- **Q3 (Abr)**: Desenvolvimento MVP
- **Q4 (Abr-Mai)**: Testes e Relatório Parcial
- **Q5-Q7 (Mai-Jun)**: Finalização e Deploy

## 📞 Contato

**Orientador**: Daniel Augusto Oliveira Massolla

**Equipe Grupo 3**:
- Douglas
- Gustavo Luche
- Gustavo Valerio Reis
- Heverton
- João Vitor
- Willian

## 📄 Licença

Projeto educacional - UNIVESP 2026

---

**Última atualização**: Maio 2026
