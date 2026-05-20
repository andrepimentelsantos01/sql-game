import sqlite3
from pathlib import Path

DATABASES_DIR = Path(__file__).resolve().parents[1] / "app" / "data" / "databases"


def reset_database(name: str) -> sqlite3.Connection:
    DATABASES_DIR.mkdir(parents=True, exist_ok=True)
    path = DATABASES_DIR / name
    if path.exists():
        path.unlink()
    return sqlite3.connect(path)


def seed_saude() -> None:
    connection = reset_database("saude.db")
    connection.executescript(
        """
        CREATE TABLE hospitais (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL
        );

        CREATE TABLE internacoes (
            id INTEGER PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            paciente_id INTEGER NOT NULL,
            data_entrada TEXT NOT NULL,
            custo_total REAL NOT NULL,
            FOREIGN KEY (hospital_id) REFERENCES hospitais(id)
        );

        CREATE TABLE consultas (
            id INTEGER PRIMARY KEY,
            especialidade TEXT NOT NULL,
            dias_espera INTEGER NOT NULL,
            status TEXT NOT NULL
        );
        """
    )
    connection.executemany(
        "INSERT INTO hospitais (id, nome, cidade) VALUES (?, ?, ?)",
        [
            (1, "Hospital Central", "São Paulo"),
            (2, "Hospital Norte", "Campinas"),
            (3, "Hospital Atlântico", "Rio de Janeiro"),
            (4, "Hospital Vida", "Belo Horizonte"),
        ],
    )
    connection.executemany(
        "INSERT INTO internacoes (hospital_id, paciente_id, data_entrada, custo_total) VALUES (?, ?, ?, ?)",
        [
            (1, 101, "2026-01-08", 180000.0),
            (1, 102, "2026-02-14", 245000.5),
            (1, 103, "2026-03-20", 308500.0),
            (2, 104, "2026-01-18", 120000.0),
            (2, 105, "2026-03-02", 156800.0),
            (3, 106, "2026-02-09", 221400.0),
            (3, 107, "2026-03-25", 198700.0),
            (4, 108, "2026-01-31", 160250.0),
            (4, 109, "2025-12-20", 999999.0),
        ],
    )
    connection.executemany(
        "INSERT INTO consultas (especialidade, dias_espera, status) VALUES (?, ?, ?)",
        [
            ("Cardiologia", 18, "realizada"),
            ("Cardiologia", 24, "realizada"),
            ("Cardiologia", 10, "cancelada"),
            ("Ortopedia", 12, "realizada"),
            ("Ortopedia", 16, "realizada"),
            ("Dermatologia", 9, "realizada"),
            ("Dermatologia", 11, "realizada"),
            ("Neurologia", 30, "realizada"),
            ("Neurologia", 27, "realizada"),
        ],
    )
    connection.commit()
    connection.close()


def seed_logistica() -> None:
    connection = reset_database("logistica.db")
    connection.executescript(
        """
        CREATE TABLE entregas (
            id INTEGER PRIMARY KEY,
            origem TEXT NOT NULL,
            destino TEXT NOT NULL,
            dias_atraso INTEGER NOT NULL,
            custo_frete REAL NOT NULL
        );

        CREATE TABLE estoque_movimentos (
            id INTEGER PRIMARY KEY,
            produto TEXT NOT NULL,
            dias_em_estoque INTEGER NOT NULL,
            quantidade INTEGER NOT NULL
        );
        """
    )
    connection.executemany(
        "INSERT INTO entregas (origem, destino, dias_atraso, custo_frete) VALUES (?, ?, ?, ?)",
        [
            ("São Paulo", "Curitiba", 2, 540.0),
            ("São Paulo", "Curitiba", 0, 510.0),
            ("São Paulo", "Curitiba", 3, 560.0),
            ("Rio de Janeiro", "Salvador", 5, 890.0),
            ("Rio de Janeiro", "Salvador", 1, 910.0),
            ("Belo Horizonte", "Vitoria", 0, 300.0),
            ("Belo Horizonte", "Vitoria", 2, 340.0),
            ("Campinas", "Goiania", 4, 720.0),
            ("Campinas", "Goiania", 6, 760.0),
            ("Campinas", "Goiania", 0, 700.0),
        ],
    )
    connection.executemany(
        "INSERT INTO estoque_movimentos (produto, dias_em_estoque, quantidade) VALUES (?, ?, ?)",
        [
            ("Monitor 27", 42, 12),
            ("Monitor 27", 36, 9),
            ("Teclado mecânico", 18, 30),
            ("Teclado mecânico", 22, 28),
            ("Cadeira ergonômica", 55, 6),
            ("Cadeira ergonômica", 61, 4),
            ("Webcam HD", 14, 35),
            ("Webcam HD", 11, 44),
        ],
    )
    connection.commit()
    connection.close()


def seed_games() -> None:
    connection = reset_database("games.db")
    connection.executescript(
        """
        CREATE TABLE sessoes_fase (
            id INTEGER PRIMARY KEY,
            jogador TEXT NOT NULL,
            fase TEXT NOT NULL,
            abandonou INTEGER NOT NULL CHECK (abandonou IN (0, 1))
        );

        CREATE TABLE partidas_personagem (
            id INTEGER PRIMARY KEY,
            personagem TEXT NOT NULL,
            venceu INTEGER NOT NULL CHECK (venceu IN (0, 1))
        );
        """
    )
    connection.executemany(
        "INSERT INTO sessoes_fase (jogador, fase, abandonou) VALUES (?, ?, ?)",
        [
            ("Ana", "Prólogo", 0),
            ("Bruno", "Prólogo", 0),
            ("Caio", "Prólogo", 0),
            ("Ana", "Mina Congelada", 1),
            ("Bruno", "Mina Congelada", 1),
            ("Caio", "Mina Congelada", 0),
            ("Duda", "Mina Congelada", 1),
            ("Eli", "Torre Solar", 0),
            ("Fabi", "Torre Solar", 1),
            ("Gus", "Torre Solar", 0),
        ],
    )
    connection.executemany(
        "INSERT INTO partidas_personagem (personagem, venceu) VALUES (?, ?)",
        [
            ("Astra", 1),
            ("Astra", 1),
            ("Astra", 0),
            ("Bruma", 1),
            ("Bruma", 0),
            ("Bruma", 0),
            ("Nix", 1),
            ("Nix", 1),
            ("Nix", 1),
            ("Nix", 0),
            ("Rook", 0),
            ("Rook", 1),
            ("Rook", 0),
        ],
    )
    connection.commit()
    connection.close()


def main() -> None:
    seed_saude()
    seed_logistica()
    seed_games()
    print(f"Bancos criados em {DATABASES_DIR}")


if __name__ == "__main__":
    main()
