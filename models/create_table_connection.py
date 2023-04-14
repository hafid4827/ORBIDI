from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a la base de datos PostgreSQL


def psql_connect(Base: object | bool = False) -> tuple[object, object]:

    # PostgreSQL database configuration
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost/prueba_tecnica"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # will allow you to create sessions to interact with the database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Create the tables in the database
    if Base:
        Base.metadata.create_all(bind=engine)

    return session
