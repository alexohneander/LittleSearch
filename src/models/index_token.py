from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class IndexToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    weight: int = Field()
