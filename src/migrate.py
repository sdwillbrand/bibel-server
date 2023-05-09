import json
import sqlite3

conn = sqlite3.connect("data/bible.db")
conn.execute('pragma journal_mode=wal')
cursor = conn.cursor()
cursor.execute("DROP TABLE nt")
cursor.execute(
        "CREATE TABLE IF NOT EXISTS nt(book VARCHAR(100) NOT NULL, chapter integer NOT NULL, verse integer NOT NULL, content TEXT NOT NULL)")

def main():
    f = open("data/NT.json", "r", encoding="utf8")
    nt = json.load(f)
    f.close()
    for book in dict.keys(nt):
        for chapter in dict.keys(nt[book]):
            for verse in nt[book][chapter]:
                content = nt[book][chapter][verse]
                cursor.execute(f"INSERT INTO nt(book,chapter,verse,content) VALUES (?,?,?,?)", (book,chapter,verse,content))
                conn.commit()

if __name__ == "__main__":
    main()