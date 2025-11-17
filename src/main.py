import os
import uvicorn

from typing import Union
from fastapi import FastAPI
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from utils.logger import get_logger, setup_logging
from utils.ngrams_tokenizer import NGramsTokenizer
from utils.prefix_tokenizer import PrefixTokenizer
from utils.word_tokenizer import WordTokenizer
import models.index_entry  # noqa: F401
import models.index_token  # noqa: F401


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Setup logging before creating the app
setup_logging()

# Create logger for this module
logger = get_logger(__name__)


def create_db_and_tables():
    logger.info("Creating database and tables...")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/search/tokenize")
def tokenize_text(text: str = Query(..., min_length=1, max_length=1000)):
    tokenizer = WordTokenizer(weight=1)
    tokens = tokenizer.tokenize(text)

    return {"tokens": [token.dict() for token in tokens]}


@app.post("/search/tokenize/ngrams")
def tokenize_ngrams(
    text: str = Query(..., min_length=1, max_length=1000),
    n: int = Query(3, ge=1, le=10),
):
    tokenizer = NGramsTokenizer(ngram_length=n, weight=1)
    tokens = tokenizer.tokenize(text)
    return {"tokens": [token.dict() for token in tokens]}


@app.post("/search/tokenize/prefixes")
def tokenize_prefixes(
    text: str = Query(..., min_length=1, max_length=1000),
    min_prefix_length: int = Query(4, ge=1, le=20),
):
    tokenizer = PrefixTokenizer(min_prefix_length=min_prefix_length, weight=5)
    tokens = tokenizer.tokenize(text)
    return {"tokens": [token.dict() for token in tokens]}


if __name__ == "__main__":
    logger.info("Starting webserver...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        log_config=None,  # Use our custom logging configuration
    )
