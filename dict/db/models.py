from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Audio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    path: str
    phrase_id: int | None = Field(default=None, foreign_key="phrase.id")
    phrase: Optional["Phrase"] = Relationship(back_populates="audios")


class Phrase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    start_line: int | None
    start_column: int | None
    end_line: int | None
    end_column: int | None
    dictionary_id: int | None = Field(default=None, foreign_key="dictionary.id")
    dictionary: Optional["Dictionary"] = Relationship(back_populates="examples")
    document_id: int | None = Field(default=None, foreign_key="document.id")
    document: Optional["Document"] = Relationship(back_populates="phrases")
    audios: List[Audio] = Relationship(back_populates="phrase")


class Dictionary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    word: str
    normalized_word: str
    meaning: str
    examples: List[Phrase] = Relationship(back_populates="dictionary")


class ListOfDictionaries(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    source: str
    language_input: str
    language_output: str
    dictionary_id: int = Field(default=None, foreign_key="dictionary.id")
    dictionary: Dictionary = Relationship()


class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    path: str
    phrases: List[Phrase] = Relationship(back_populates="document")


class ListOfDocuments(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
