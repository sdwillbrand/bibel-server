import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class QueryBody(BaseModel):
    book: str
    chapter: int|None = None
    verse: int|None = None

app = FastAPI()

origins = [
    "http://localhost:8080",
]

connection = sqlite3.connect("../data/bible.db")
cursor = connection.cursor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_bible(req: QueryBody):
    book = req.book
    chapter = req.chapter
    verse = req.verse
    res = cursor.execute(f"select content, chapter, verse from nt where book='{book}' {'and chapter=' + str(chapter) if chapter else ''} {'and verse=' + str(verse) if verse else ''} union select content, chapter, verse from at where book='{book}' {'and chapter=' + str(chapter) if chapter else ''} {'and verse=' + str(verse) if verse else ''} order by chapter, verse")
    content = res.fetchall()
    return content

@app.get("/books")
async def get_books():
    res = cursor.execute(f"select distinct book from at union select distinct book from nt")
    books = res.fetchall()
    return books

@app.get("/")
async def read_root():
    return "Preist den HERRn!"