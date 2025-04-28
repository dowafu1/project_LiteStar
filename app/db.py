from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig, SQLAlchemyPlugin, AsyncSessionConfig
from advanced_alchemy.base import UUIDBase

# Конфигурация БД
alchemy = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///./test.db",  # Путь к базе данных SQLite
    before_send_handler="autocommit",  # Настройка автокоммита
    session_config=AsyncSessionConfig(expire_on_commit=False),  # Конфигурация сессии
    create_all=True,  # Создаёт все таблицы, если они не существуют
)

# Плагин для подключения к Litestar
alchemy_plugin = SQLAlchemyPlugin(config=alchemy)

# Базовый класс моделей
Base = UUIDBase
