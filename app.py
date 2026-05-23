import os
import psycopg
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-change-this-secret-key')

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', f'{ADMIN_USERNAME}@admin.local')

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')


def is_safe_redirect_target(target):
    """Permite redirecionamentos apenas internos."""
    return bool(target) and target.startswith('/') and not target.startswith('//')


def validate_admin_credentials(username, password):
    """Valida login administrativo usando usuario persistido no banco."""
    conn = get_db_connection()
    if not conn:
        return False, 'Erro ao conectar ao banco.'

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT senha_hash, ativo
            FROM usuarios
            WHERE username = %s
            """,
            (username,)
        )
        row = cur.fetchone()
        cur.close()
    except Exception:
        conn.close()
        return False, 'Erro ao validar usuario no banco.'

    conn.close()

    if not row:
        return False, None

    senha_hash, ativo = row
    if not ativo:
        return False, None

    return check_password_hash(senha_hash, password), None


def admin_required(view_func):
    """Protege rotas administrativas via sessão."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if session.get('is_admin_authenticated'):
            return view_func(*args, **kwargs)

        if request.path.startswith('/api/admin/'):
            return jsonify({'erro': 'Nao autorizado'}), 401

        return redirect(url_for('admin_login', next=request.path))

    return wrapped

def get_db_connection():
    """Estabelecer conexão com PostgreSQL"""
    try:
        conn = psycopg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None


def init_db():
    """Cria estrutura mínima do banco na inicialização do app."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS falecidos (
                id SERIAL PRIMARY KEY,
                nome_falecido VARCHAR(255) NOT NULL,
                data_nascimento DATE,
                data_falecimento DATE,
                cemiterio VARCHAR(255) DEFAULT 'Cemitério da Igualdade',
                setor VARCHAR(50) NOT NULL,
                quadra VARCHAR(50) NOT NULL,
                jazigo VARCHAR(50) NOT NULL,
                observacoes TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                ativo BOOLEAN DEFAULT true,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute("ALTER TABLE falecidos ADD COLUMN IF NOT EXISTS data_nascimento DATE")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_falecidos_nome ON falecidos (nome_falecido)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_falecidos_setor_quadra ON falecidos (setor, quadra)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_falecidos_jazigo ON falecidos (jazigo)")

        # Cria um admin inicial para permitir acesso ao painel.
        cur.execute("SELECT id FROM usuarios WHERE username = %s", (ADMIN_USERNAME,))
        usuario_admin = cur.fetchone()
        if not usuario_admin:
            cur.execute(
                """
                INSERT INTO usuarios (username, email, senha_hash, ativo)
                VALUES (%s, %s, %s, true)
                ON CONFLICT (username) DO NOTHING
                """,
                (ADMIN_USERNAME, ADMIN_EMAIL, generate_password_hash(ADMIN_PASSWORD))
            )

        conn.commit()
        cur.close()
    finally:
        conn.close()


init_db()

@app.route('/')
def index():
    """Página inicial com formulário de busca"""
    return render_template('index.html')

@app.route('/api/buscar', methods=['POST'])
def buscar():
    """API para buscar falecidos"""
    try:
        data = request.get_json() or {}
        nome = data.get('nome', '').strip()
        lapide = data.get('lapide', '').strip()
        setor = data.get('setor', '').strip()
        quadra = data.get('quadra', '').strip()
        data_falecimento_de = data.get('data_falecimento_de')
        data_falecimento_ate = data.get('data_falecimento_ate')

        if not any([nome, lapide, setor, quadra, data_falecimento_de, data_falecimento_ate]):
            return jsonify({'erro': 'Informe pelo menos um filtro para buscar'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500
        
        cur = conn.cursor()
        query = """
            SELECT id, nome_falecido, data_nascimento, data_falecimento, setor, quadra, jazigo, observacoes
            FROM falecidos
            WHERE 1=1
        """

        params = []

        if nome:
            query += " AND LOWER(nome_falecido) LIKE LOWER(%s)"
            params.append(f'%{nome}%')

        if lapide:
            query += " AND LOWER(jazigo) LIKE LOWER(%s)"
            params.append(f'%{lapide}%')

        if setor:
            query += " AND LOWER(setor) = LOWER(%s)"
            params.append(setor)

        if quadra:
            query += " AND LOWER(quadra) LIKE LOWER(%s)"
            params.append(f'%{quadra}%')

        if data_falecimento_de:
            query += " AND data_falecimento >= %s"
            params.append(data_falecimento_de)

        if data_falecimento_ate:
            query += " AND data_falecimento <= %s"
            params.append(data_falecimento_ate)

        query += " ORDER BY nome_falecido"

        cur.execute(query, tuple(params))
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        
        if not resultados:
            return jsonify({'mensagem': 'Nenhum resultado encontrado'}), 200
        
        return jsonify({
            'total': len(resultados),
            'resultados': [
                {
                    'id': r[0],
                    'nome': r[1],
                    'data_nascimento': r[2].isoformat() if r[2] else None,
                    'data_falecimento': r[3].isoformat() if r[3] else None,
                    'setor': r[4],
                    'quadra': r[5],
                    'jazigo': r[6],
                    'observacoes': r[7]
                }
                for r in resultados
            ]
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/filtros', methods=['GET'])
def filtros_busca():
    """Retorna opções para os filtros de busca."""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500

        cur = conn.cursor()
        cur.execute("SELECT DISTINCT setor FROM falecidos WHERE setor IS NOT NULL AND setor <> '' ORDER BY setor")
        setores = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT quadra FROM falecidos WHERE quadra IS NOT NULL AND quadra <> '' ORDER BY quadra")
        quadras = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return jsonify({'setores': setores, 'quadras': quadras}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/admin')
@admin_required
def admin():
    """Página do painel administrativo."""
    return render_template('admin.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Login administrativo."""
    if session.get('is_admin_authenticated'):
        return redirect(url_for('admin'))

    erro = None
    next_target = request.args.get('next', '/admin')
    if not is_safe_redirect_target(next_target):
        next_target = '/admin'

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        form_next = request.form.get('next', '')

        is_valid, auth_error = validate_admin_credentials(username, password)
        if is_valid:
            session['is_admin_authenticated'] = True
            session['admin_username'] = username

            target = form_next if is_safe_redirect_target(form_next) else '/admin'
            return redirect(target)

        erro = auth_error or 'Usuario ou senha invalidos.'

    return render_template('admin_login.html', erro=erro, next_target=next_target)


@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Logout administrativo."""
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/api/admin/registros', methods=['GET'])
@admin_required
def listar_registros():
    """API para listar registros com paginação (admin)"""
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        nome = request.args.get('nome', default='', type=str).strip()
        setor = request.args.get('setor', default='', type=str).strip()
        quadra = request.args.get('quadra', default='', type=str).strip()

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:
            per_page = 100

        offset = (page - 1) * per_page

        where_clauses = []
        where_params = []

        if nome:
            where_clauses.append("LOWER(nome_falecido) LIKE LOWER(%s)")
            where_params.append(f"%{nome}%")

        if setor:
            where_clauses.append("LOWER(setor) LIKE LOWER(%s)")
            where_params.append(f"%{setor}%")

        if quadra:
            where_clauses.append("LOWER(quadra) LIKE LOWER(%s)")
            where_params.append(f"%{quadra}%")

        where_sql = ""
        if where_clauses:
            where_sql = " WHERE " + " AND ".join(where_clauses)

        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500
        
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM falecidos{where_sql}", tuple(where_params))
        total = cur.fetchone()[0]

        query_params = list(where_params)
        query_params.extend([per_page, offset])
        cur.execute(
            f"""
            SELECT id, nome_falecido, data_nascimento, data_falecimento, setor, quadra, jazigo, observacoes
            FROM falecidos
            {where_sql}
            ORDER BY nome_falecido
            LIMIT %s OFFSET %s
            """
            , tuple(query_params)
        )
        registros = cur.fetchall()
        cur.close()
        conn.close()

        total_paginas = (total + per_page - 1) // per_page if total > 0 else 0
        
        return jsonify({
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_paginas': total_paginas,
            'registros': [
                {
                    'id': r[0],
                    'nome': r[1],
                    'data_nascimento': r[2].isoformat() if r[2] else None,
                    'data_falecimento': r[3].isoformat() if r[3] else None,
                    'setor': r[4],
                    'quadra': r[5],
                    'jazigo': r[6],
                    'observacoes': r[7]
                }
                for r in registros
            ]
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/adicionar', methods=['POST'])
@admin_required
def adicionar_registro():
    """API para adicionar novo registro"""
    try:
        data = request.get_json()
        nome = data.get('nome_falecido', '').strip()
        setor = data.get('setor', '').strip()
        quadra = data.get('quadra', '').strip()
        jazigo = data.get('jazigo', '').strip()
        
        # Validação básica
        if not all([nome, setor, quadra, jazigo]):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500
        
        cur = conn.cursor()
        query = """
            INSERT INTO falecidos (
                nome_falecido,
                data_nascimento,
                data_falecimento,
                setor,
                quadra,
                jazigo,
                observacoes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cur.execute(query, (
            nome,
            data.get('data_nascimento'),
            data.get('data_falecimento'),
            setor,
            quadra,
            jazigo,
            data.get('observacoes', '')
        ))
        novo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'mensagem': 'Registro adicionado com sucesso', 'id': novo_id}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/editar/<int:id>', methods=['PUT'])
@admin_required
def editar_registro(id):
    """API para editar registro"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500
        
        cur = conn.cursor()
        query = """
            UPDATE falecidos
            SET nome_falecido = %s,
                data_nascimento = %s,
                data_falecimento = %s,
                setor = %s,
                quadra = %s,
                jazigo = %s,
                observacoes = %s,
                data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cur.execute(query, (
            data.get('nome_falecido'),
            data.get('data_nascimento'),
            data.get('data_falecimento'),
            data.get('setor'),
            data.get('quadra'),
            data.get('jazigo'),
            data.get('observacoes'),
            id
        ))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'mensagem': 'Registro atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/deletar/<int:id>', methods=['DELETE'])
@admin_required
def deletar_registro(id):
    """API para deletar registro"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500
        
        cur = conn.cursor()
        cur.execute("DELETE FROM falecidos WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'mensagem': 'Registro deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/health')
def health():
    """Health check para monitoramento"""
    return jsonify({'status': 'online', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True', 
            host='0.0.0.0', 
            port=int(os.getenv('PORT', 5000)))
