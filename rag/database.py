from sqlalchemy import create_engine, text
from rag.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)

def check_connection() -> None:
    """
    Проверяет подключение к PostgreSQL.

    Получаем:
    - название текущей БД;
    - имя текущего пользователя.
    """

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    current_database(),
                    current_user
                """)
        )

        row = result.one()

        database_name = row[0]
        user_name = row[1]

        print(
            f"Подключение к PostgreSQL успешно.\n"
            f"База данных: {database_name}\n"
            f"Пользователь: {user_name}"
        )
