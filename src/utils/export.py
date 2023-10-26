from main import cursor, get_books
from const import abbrevations
import asyncio

async def main():
    books = await get_books()
    with open("../data/export.csv", "w", encoding="utf8") as file:
        csv = ""
        for (i,book) in enumerate(books):
            res = cursor.execute(f"select chapter, verse, content from nt where nt.book='{book}' union select chapter, verse, content from at where at.book='{book}'")
            contents = res.fetchall()
            for (chapter, verse, content) in contents:
                abbr = abbrevations[i]
                csv += f"{abbr}. {chapter},{verse}|{content}|{book}\r"
        file.write(csv)

asyncio.run(main())