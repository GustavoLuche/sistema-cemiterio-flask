import os
import psycopg2
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    """Estabelecer conexão com PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

@app.route('/')
def index():
    """Página inicial com formulário de busca"""
    return render_template('index.html')

@app.route('/api/buscar', methods=['POST'])
def buscar():
    """API para buscar falecidos"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        
        if not nome:
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500
        
        cur = conn.cursor()
        # Busca case-insensitive com LIKE
        query = """
            SELECT id, nome_falecido, data_falecimento, setor, quadra, jazigo, observacoes
            FROM falecidos
            WHERE LOWER(nome_falecido) LIKE LOWER(%s)
            ORDER BY nome_falecido
        """
        cur.execute(query, (f'%{nome}%',))
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
                    'data_falecimento': r[2].isoformat() if r[2] else None,
                    'setor': r[3],
                    'quadra': r[4],
                    'jazigo': r[5],
                    'observacoes': r[6]
                }
                for r in resultados
            ]
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/admin')
def admin():
    """Página do painel administrativo (futuro: adicionar autenticação)"""
    return render_template('admin.html')

@app.route('/api/admin/registros', methods=['GET'])
def listar_registros():
    """API para listar todos os registros (admin)"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'erro': 'Erro ao conectar ao banco'}), 500
        
        cur = conn.cursor()
        cur.execute("SELECT id, nome_falecido, setor, quadra, jazigo FROM falecidos ORDER BY nome_falecido")
        registros = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            'total': len(registros),
            'registros': [
                {
                    'id': r[0],
                    'nome': r[1],
                    'setor': r[2],
                    'quadra': r[3],
                    'jazigo': r[4]
                }
                for r in registros
            ]
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/adicionar', methods=['POST'])
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
            INSERT INTO falecidos (nome_falecido, setor, quadra, jazigo, observacoes, data_falecimento)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cur.execute(query, (
            nome, setor, quadra, jazigo, 
            data.get('observacoes', ''),
            data.get('data_falecimento')
        ))
        novo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'mensagem': 'Registro adicionado com sucesso', 'id': novo_id}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/editar/<int:id>', methods=['PUT'])
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
            SET nome_falecido = %s, setor = %s, quadra = %s, jazigo = %s, 
                observacoes = %s, data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cur.execute(query, (
            data.get('nome_falecido'),
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
