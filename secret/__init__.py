import os


def get_db_url(database_id: int) -> str:
    return os.getenv('REDISTOGO_URL', f'redis://localhost:7777/{database_id}')
