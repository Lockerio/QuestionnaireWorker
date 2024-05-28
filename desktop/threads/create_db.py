from app.database.db import Base, engine


def create_db(progress_callback):
    progress_callback.emit("Создаем базу данных")
    Base.metadata.create_all(engine, checkfirst=True)
    progress_callback.emit("База данных создана")
