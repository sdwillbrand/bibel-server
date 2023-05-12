import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import randint
class QueryBody(BaseModel):
    book: str
    chapter: int|None = None
    verse: int|None = None

app = FastAPI()

origins = [
    "http://localhost:3000",
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
    contents = res.fetchall()
    return contents

@app.get("/books")
async def get_books():
    res = cursor.execute(f"select title from book order by book.id")
    books = res.fetchall()
    return [title for [title] in books]

@app.get("/chapter_count/{book}")
async def get_chapters_count(book:str):
    res = cursor.execute(f"select count(distinct at.chapter) from at where at.book='{book}'")
    amount = res.fetchone()[0]
    res = cursor.execute(f"select count(distinct nt.chapter) from nt where nt.book='{book}'")
    amount += res.fetchone()[0]
    return amount

@app.get("/verse_count/{book}/{chapter}")
async def get_verses_count(book:str, chapter:int):
    res = cursor.execute(f"select count(distinct at.verse) from at where at.book='{book}' and at.chapter={chapter}")
    amount = res.fetchone()[0]
    res = cursor.execute(f"select count(distinct nt.verse) from nt where nt.book='{book}' and nt.chapter={chapter}")
    amount += res.fetchone()[0]
    return amount
    
@app.get("/random_verse")
async def get_random_verse():
    books = await get_books()
    i = randint(0, len(books) -1)
    book = books[i]
    count = await get_chapters_count(book)
    chapter = randint(0, count-1)
    count = await get_verses_count(book, chapter)
    verse = randint(0, count-1)
    res = await query_bible(QueryBody(book=book,chapter=chapter, verse=verse))
    return {"content":res[0][0], "chapter": chapter, "verse": verse, "book": book}
    
    

@app.get("/")
async def read_root():
    return "Preist den HERRn!"