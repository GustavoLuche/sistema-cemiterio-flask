-- Criar tabela de registros de falecidos
CREATE TABLE IF NOT EXISTS falecidos (
    id SERIAL PRIMARY KEY,
    nome_falecido VARCHAR(255) NOT NULL,
    data_falecimento DATE,
    cemiterio VARCHAR(255) DEFAULT 'Cemitério da Igualdade',
    setor VARCHAR(50) NOT NULL,
    quadra VARCHAR(50) NOT NULL,
    jazigo VARCHAR(50) NOT NULL,
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de usuários admin (para futuro)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT true,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_falecidos_nome ON falecidos (nome_falecido);
CREATE INDEX IF NOT EXISTS idx_falecidos_setor_quadra ON falecidos (setor, quadra);
CREATE INDEX IF NOT EXISTS idx_falecidos_jazigo ON falecidos (jazigo);
