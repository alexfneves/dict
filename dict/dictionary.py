from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select

from dict.settings import Settings


def default_dictionary():
    return ("en", "en")


def list_of_dictionaries():
    return [
        ("da", "da"),
        ("da", "en"),
        ("da", "pt_br"),
        ("en", "da"),
        ("en", "en"),
        ("en", "pt_br"),
        ("pt_br", "da"),
        ("pt_br", "en"),
        ("pt_br", "pt_br"),
    ]


engine = None


def create_db():
    settings = Settings()
    sqlite_file_name = Path.joinpath(settings._data_path, "en.db")
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    global engine
    engine = create_engine(sqlite_url, echo=True)

    SQLModel.metadata.create_all(engine)


def create_words():
    global engine

    # cleanup
    with Session(engine) as session:
        statement = select(Word)
        results = session.exec(statement)
        for r in results:
            session.delete(r)
        session.commit()

    # define words
    w_this = Word(word="this", meaning="The meaning of word this")
    w_is = Word(word="this", meaning="The meaning of word is")
    w_a = Word(word="this", meaning="The meaning of word a")
    w_dictionary = Word(word="this", meaning="The meaning of word dictionary")

    # add new words to the database
    with Session(engine) as session:
        session.add(w_this)
        session.add(w_is)
        session.add(w_a)
        session.add(w_dictionary)
        session.commit()


class Word(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    word: str
    meaning: str
