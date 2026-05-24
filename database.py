from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Путь к файлу базы данных
DATABASE_URL = "sqlite:///./memory.db"

# Engine — это "соединение" с БД
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # нужно для SQLite в многопоточном FastAPI
)

# SessionLocal — фабрика сессий для каждого запроса
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Эта функция отдаёт сессию БД для одного запроса.
    После запроса сессия автоматически закрывается.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Создаёт все таблицы в БД (если ещё не созданы).
    Это для первого запуска. Потом будем использовать Alembic для миграций.
    """
    Base.metadata.create_all(bind=engine)
