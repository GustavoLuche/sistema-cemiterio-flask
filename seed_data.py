import os
from datetime import date

import psycopg
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def derive_birth_date(data_falecimento, idade_estimada=70):
    """Gera uma data de nascimento aproximada quando não houver valor explícito."""
    if not data_falecimento:
        return None

    year = max(1900, data_falecimento.year - idade_estimada)
    day = min(data_falecimento.day, 28)
    return date(year, data_falecimento.month, day)


SAMPLE_RECORDS = [
    {
        "nome_falecido": "Maria Aparecida dos Santos",
        "data_falecimento": date(2018, 7, 22),
        "setor": "A",
        "quadra": "A1",
        "jazigo": "A-001",
        "observacoes": "Registro ficticio para demonstracao do sistema.",
    },
    {
        "nome_falecido": "Jose Carlos Oliveira",
        "data_falecimento": date(2020, 1, 15),
        "setor": "A",
        "quadra": "A1",
        "jazigo": "A-002",
        "observacoes": "Familia Oliveira. Dados de exemplo.",
    },
    {
        "nome_falecido": "Ana Luiza Pereira",
        "data_falecimento": date(2021, 8, 3),
        "setor": "A",
        "quadra": "A1",
        "jazigo": "A-003",
        "observacoes": "Registro ficticio para testes de busca.",
    },
    {
        "nome_falecido": "Francisco Rodrigues Neto",
        "data_falecimento": date(2017, 12, 30),
        "setor": "A",
        "quadra": "A1",
        "jazigo": "A-004",
        "observacoes": "Dados ilustrativos do setor A.",
    },
    {
        "nome_falecido": "Benedita Silva Ferreira",
        "data_falecimento": date(2022, 5, 10),
        "setor": "A",
        "quadra": "A1",
        "jazigo": "A-005",
        "observacoes": "Cadastro demonstrativo.",
    },
    {
        "nome_falecido": "Joao Batista Almeida",
        "data_falecimento": date(2019, 3, 28),
        "setor": "A",
        "quadra": "A2",
        "jazigo": "A-006",
        "observacoes": "Cadastro demonstrativo.",
    },
    {
        "nome_falecido": "Tereza de Jesus Lima",
        "data_falecimento": date(2023, 2, 14),
        "setor": "A",
        "quadra": "A2",
        "jazigo": "A-007",
        "observacoes": "Dados ficticios para validacao de interface.",
    },
    {
        "nome_falecido": "Manoel Costa Barbosa",
        "data_falecimento": date(2016, 9, 5),
        "setor": "A",
        "quadra": "A2",
        "jazigo": "A-008",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Luiza Helena Souza",
        "data_falecimento": date(2024, 6, 1),
        "setor": "A",
        "quadra": "A2",
        "jazigo": "A-009",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Raimundo Nonato Carvalho",
        "data_falecimento": date(2022, 11, 19),
        "setor": "A",
        "quadra": "A2",
        "jazigo": "A-010",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Sebastiana Matos Gomes",
        "data_falecimento": date(2020, 8, 17),
        "setor": "A",
        "quadra": "A3",
        "jazigo": "A-011",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Pedro Henrique Martins",
        "data_falecimento": date(2021, 4, 30),
        "setor": "A",
        "quadra": "A3",
        "jazigo": "A-012",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Conceicao Ribeiro Teixeira",
        "data_falecimento": date(2023, 9, 22),
        "setor": "A",
        "quadra": "A3",
        "jazigo": "A-013",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Antonio Ferreira de Moraes",
        "data_falecimento": date(2018, 1, 7),
        "setor": "A",
        "quadra": "A3",
        "jazigo": "A-014",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Fatima Vieira Nascimento",
        "data_falecimento": date(2024, 3, 11),
        "setor": "A",
        "quadra": "A3",
        "jazigo": "A-015",
        "observacoes": "Registro ficticio.",
    },
    {
        "nome_falecido": "Roberto Carlos Mendes",
        "data_falecimento": date(2023, 12, 5),
        "setor": "B",
        "quadra": "B1",
        "jazigo": "B-001",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Irene Cardoso Pinto",
        "data_falecimento": date(2015, 7, 30),
        "setor": "B",
        "quadra": "B1",
        "jazigo": "B-002",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Domingos Lopes Aguiar",
        "data_falecimento": date(2019, 10, 14),
        "setor": "B",
        "quadra": "B1",
        "jazigo": "B-003",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Rosaria Cunha Figueiredo",
        "data_falecimento": date(2022, 2, 28),
        "setor": "B",
        "quadra": "B1",
        "jazigo": "B-004",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Valmir Sousa Guimaraes",
        "data_falecimento": date(2020, 5, 19),
        "setor": "B",
        "quadra": "B1",
        "jazigo": "B-005",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Aparecida Machado Torres",
        "data_falecimento": date(2017, 4, 3),
        "setor": "B",
        "quadra": "B1",
        "jazigo": "B-006",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Gilberto Araujo Fontes",
        "data_falecimento": date(2021, 11, 12),
        "setor": "B",
        "quadra": "B2",
        "jazigo": "B-007",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Neide Santos Duarte",
        "data_falecimento": date(2023, 7, 8),
        "setor": "B",
        "quadra": "B2",
        "jazigo": "B-008",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Altair Ramos Correa",
        "data_falecimento": date(2018, 9, 25),
        "setor": "B",
        "quadra": "B2",
        "jazigo": "B-009",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Dulce Maria Pires",
        "data_falecimento": date(2024, 1, 20),
        "setor": "B",
        "quadra": "B2",
        "jazigo": "B-010",
        "observacoes": "Registro ficticio do setor B.",
    },
    {
        "nome_falecido": "Osvaldo Braga Monteiro",
        "data_falecimento": date(2016, 5, 4),
        "setor": "C",
        "quadra": "C1",
        "jazigo": "C-001",
        "observacoes": "Registro ficticio do setor C.",
    },
    {
        "nome_falecido": "Lucia Campos Andrade",
        "data_falecimento": date(2019, 12, 16),
        "setor": "C",
        "quadra": "C1",
        "jazigo": "C-002",
        "observacoes": "Registro ficticio do setor C.",
    },
    {
        "nome_falecido": "Waldir Tavares Dias",
        "data_falecimento": date(2022, 8, 30),
        "setor": "C",
        "quadra": "C1",
        "jazigo": "C-003",
        "observacoes": "Registro ficticio do setor C.",
    },
    {
        "nome_falecido": "Helia Moreira Bastos",
        "data_falecimento": date(2023, 4, 17),
        "setor": "C",
        "quadra": "C1",
        "jazigo": "C-004",
        "observacoes": "Registro ficticio do setor C.",
    },
    {
        "nome_falecido": "Dirceu Alves Siqueira",
        "data_falecimento": date(2021, 1, 28),
        "setor": "C",
        "quadra": "C1",
        "jazigo": "C-005",
        "observacoes": "Registro ficticio do setor C.",
    },
    {
        "nome_falecido": "Elza Couto Magalhaes",
        "data_falecimento": date(2020, 10, 9),
        "setor": "D",
        "quadra": "D1",
        "jazigo": "D-001",
        "observacoes": "Registro ficticio do setor D.",
    },
    {
        "nome_falecido": "Wanderley Prado Leite",
        "data_falecimento": date(2024, 2, 25),
        "setor": "D",
        "quadra": "D1",
        "jazigo": "D-002",
        "observacoes": "Registro ficticio do setor D.",
    },
    {
        "nome_falecido": "Iraci Brito Cavalcante",
        "data_falecimento": date(2017, 6, 13),
        "setor": "D",
        "quadra": "D1",
        "jazigo": "D-003",
        "observacoes": "Registro ficticio do setor D.",
    },
    {
        "nome_falecido": "Herminio Freitas Dantas",
        "data_falecimento": date(2022, 12, 8),
        "setor": "D",
        "quadra": "D1",
        "jazigo": "D-004",
        "observacoes": "Registro ficticio do setor D.",
    },
    {
        "nome_falecido": "Celeste Rodrigues Paiva",
        "data_falecimento": date(2023, 10, 31),
        "setor": "D",
        "quadra": "D1",
        "jazigo": "D-005",
        "observacoes": "Registro ficticio do setor D.",
    },
]


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL nao definida. Configure o arquivo .env ou a variavel de ambiente.")
    return psycopg.connect(DATABASE_URL)


def seed_falecidos():
    inserted = 0
    skipped = 0
    backfilled = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            for record in SAMPLE_RECORDS:
                cur.execute(
                    """
                    SELECT id, data_nascimento, data_falecimento
                    FROM falecidos
                    WHERE nome_falecido = %s
                      AND setor = %s
                      AND quadra = %s
                      AND jazigo = %s
                    LIMIT 1
                    """,
                    (
                        record["nome_falecido"],
                        record["setor"],
                        record["quadra"],
                        record["jazigo"],
                    ),
                )
                exists = cur.fetchone()

                if exists:
                    skipped += 1

                    existing_id, existing_birth, existing_death = exists
                    if not existing_birth:
                        birth = record.get("data_nascimento") or derive_birth_date(
                            record.get("data_falecimento") or existing_death
                        )
                        if birth:
                            cur.execute(
                                """
                                UPDATE falecidos
                                SET data_nascimento = %s,
                                    data_atualizacao = CURRENT_TIMESTAMP
                                WHERE id = %s
                                """,
                                (birth, existing_id),
                            )
                            backfilled += 1
                    continue

                cur.execute(
                    """
                    INSERT INTO falecidos (
                        nome_falecido,
                        data_nascimento,
                        data_falecimento,
                        setor,
                        quadra,
                        jazigo,
                        observacoes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        record["nome_falecido"],
                        record.get("data_nascimento") or derive_birth_date(record.get("data_falecimento")),
                        record["data_falecimento"],
                        record["setor"],
                        record["quadra"],
                        record["jazigo"],
                        record["observacoes"],
                    ),
                )
                inserted += 1

        conn.commit()

    print(
        f"Seed concluido. Inseridos: {inserted}. Ja existentes: {skipped}. "
        f"Nascimento preenchido: {backfilled}."
    )


if __name__ == "__main__":
    seed_falecidos()