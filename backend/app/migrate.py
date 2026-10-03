import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = PROJECT_ROOT / "migrations"


def run_migrations():
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    if not migration_files:
        print("No migration files found.")
        return

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255) UNIQUE NOT NULL,
                    applied_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

            for migration_file in migration_files:

                filename = migration_file.name

                cursor.execute(
                    """
                    SELECT 1
                    FROM schema_migrations
                    WHERE filename = %s;
                    """,
                    (filename,)
                )

                if cursor.fetchone():
                    print(f"Skipping {filename}")
                    continue

                print(f"Running {filename}")

                sql = migration_file.read_text(encoding="utf-8")

                cursor.execute(sql)

                cursor.execute(
                    """
                    INSERT INTO schema_migrations (filename)
                    VALUES (%s);
                    """,
                    (filename,)
                )

                print(f"Applied {filename}")

        connection.commit()

    print("Migrations completed successfully.")


if __name__ == "__main__":
    run_migrations()