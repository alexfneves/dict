from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

from dict.db import models
from dict.settings import Settings

engine = None


def create_db():
    settings = Settings()
    sqlite_file_name = Path.joinpath(settings._data_path, "main.db")
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    global engine
    engine = create_engine(sqlite_url)

    SQLModel.metadata.create_all(engine)


def cleanup(table):
    global engine

    with Session(engine) as session:
        statement = select(table)
        results = session.exec(statement)
        for r in results:
            session.delete(r)
        session.commit()


def fillout_db():
    global engine

    # cleanup
    cleanup(models.Audio)
    cleanup(models.Phrase)
    cleanup(models.Dictionary)
    cleanup(models.ListOfDictionaries)
    cleanup(models.Document)
    cleanup(models.ListOfDocuments)

    # fillout
    d_some_doc = models.Document(path="some/path")
    models.Phrase(
        text="Example phrase",
        start_line=1,
        start_column=5,
        end_line=1,
        end_column=20,
        document=d_some_doc,
    )

    with Session(engine) as session:
        session.add(d_some_doc)
        session.commit()

        document = session.get(models.Document, d_some_doc.id)
        print(f"Document path: {document.path}")
        print("Associated Phrases:")
        for phrase in document.phrases:
            print(f"- {phrase.text}")
