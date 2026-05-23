import os
import random
from datetime import date, timedelta

import psycopg
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

SETORES_VALIDOS = ("A", "B", "C", "D")
QUADRAS_POR_SETOR = {setor: [f"{setor}{indice}" for indice in range(1, 11)] for setor in SETORES_VALIDOS}

PRIMEIROS_NOMES = [
    "Ana", "Maria", "Joao", "Jose", "Carlos", "Paulo", "Claudia", "Fernanda", "Rita", "Juliana",
    "Marcos", "Patricia", "Silvia", "Luciana", "Antonio", "Francisco", "Roberta", "Sandra", "Pedro", "Luiz",
]

NOMES_MEIO = [
    "Aparecida", "Cristina", "Eduardo", "Henrique", "Luiza", "Camila", "Tereza", "Fabio", "Celso", "Vera",
    "Helena", "Mateus", "Carolina", "Beatriz", "Almeida", "Couto", "Pereira", "Lima", "Souza", "Andrade",
]

SOBRENOMES = [
    "Santos", "Oliveira", "Silva", "Pereira", "Lopes", "Almeida", "Ribeiro", "Mendes", "Carvalho", "Ferreira",
    "Matos", "Gomes", "Torres", "Monteiro", "Teixeira", "Nogueira", "Prado", "Bastos", "Barbosa", "Araujo",
]


def derive_birth_date(data_falecimento, idade_estimada=70):
    """Gera uma data de nascimento aproximada quando não houver valor explícito."""
    if not data_falecimento:
        return None

    year = max(1900, data_falecimento.year - idade_estimada)
    day = min(data_falecimento.day, 28)
    return date(year, data_falecimento.month, day)


def generate_bulk_records(total=1000, seed=20260523):
    """Gera registros fictícios adicionais restritos aos setores A-D."""
    rng = random.Random(seed)
    records = []
    start_death = date(2010, 1, 1)
    death_range_days = (date(2025, 12, 31) - start_death).days

    for index in range(total):
        setor = SETORES_VALIDOS[index % len(SETORES_VALIDOS)]
        quadra = rng.choice(QUADRAS_POR_SETOR[setor])
        jazigo = f"{setor}-{1000 + index:04d}"

        nome = (
            f"{rng.choice(PRIMEIROS_NOMES)} "
            f"{rng.choice(NOMES_MEIO)} "
            f"{rng.choice(SOBRENOMES)}"
        )

        data_falecimento = start_death + timedelta(days=rng.randint(0, death_range_days))
        idade = rng.randint(45, 97)

        records.append(
            {
                "nome_falecido": nome,
                "data_nascimento": derive_birth_date(data_falecimento, idade_estimada=idade),
                "data_falecimento": data_falecimento,
                "setor": setor,
                "quadra": quadra,
                "jazigo": jazigo,
                "observacoes": "Registro ficticio gerado automaticamente para testes do sistema.",
            }
        )

    return records


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
    records_to_seed = SAMPLE_RECORDS + generate_bulk_records(total=1000)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nome_falecido, setor, quadra, jazigo, data_nascimento, data_falecimento
                FROM falecidos
                """
            )
            existing_rows = cur.fetchall()

            existing_index = {
                (row[1], row[2], row[3], row[4]): {
                    "id": row[0],
                    "data_nascimento": row[5],
                    "data_falecimento": row[6],
                }
                for row in existing_rows
            }

            insert_params = []
            update_params = []

            for record in records_to_seed:
                key = (record["nome_falecido"], record["setor"], record["quadra"], record["jazigo"])
                existing = existing_index.get(key)

                if existing:
                    skipped += 1
                    if not existing["data_nascimento"]:
                        birth = record.get("data_nascimento") or derive_birth_date(
                            record.get("data_falecimento") or existing["data_falecimento"]
                        )
                        if birth:
                            update_params.append((birth, existing["id"]))
                            backfilled += 1
                    continue

                insert_params.append(
                    (
                        record["nome_falecido"],
                        record.get("data_nascimento") or derive_birth_date(record.get("data_falecimento")),
                        record["data_falecimento"],
                        record["setor"],
                        record["quadra"],
                        record["jazigo"],
                        record["observacoes"],
                    )
                )

            if update_params:
                cur.executemany(
                    """
                    UPDATE falecidos
                    SET data_nascimento = %s,
                        data_atualizacao = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    update_params,
                )

            if insert_params:
                cur.executemany(
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
                    insert_params,
                )

            inserted = len(insert_params)

        conn.commit()

    print(
        f"Seed concluido. Total processado: {len(records_to_seed)}. "
        f"Inseridos: {inserted}. Ja existentes: {skipped}. "
        f"Nascimento preenchido: {backfilled}."
    )


if __name__ == "__main__":
    seed_falecidos()