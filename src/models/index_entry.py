from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class IndexEntry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token_id: int = Field(index=True)
    document_type: int = Field(index=True)
    field_id: int = Field(index=True)
    document_id: int = Field(index=True)
    weight: int = Field(index=True)
