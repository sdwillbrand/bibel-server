import json
import sqlite3

conn = sqlite3.connect("../../data/bible.db")
conn.execute('pragma journal_mode=wal')
cursor = conn.cursor()

def main():
    tstms = [("AT.json", "at"), ("NT.json", "nt")]
    for (file_name, db) in tstms:
        cursor.execute(f"DROP TABLE {db}")
        cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {db}(book VARCHAR(100) NOT NULL, chapter integer NOT NULL, verse integer NOT NULL, content TEXT NOT NULL)")
        f = open(f"../data/{file_name}", "r", encoding="utf8")
        bible = json.load(f)
        f.close()
        for book in dict.keys(bible):
            for chapter in dict.keys(bible[book]):
                for verse in bible[book][chapter]:
                    content = bible[book][chapter][verse]
                    cursor.execute(f"INSERT INTO {db}(book,chapter,verse,content) VALUES (?,?,?,?)", (book,chapter,verse,content))
                    conn.commit()

if __name__ == "__main__":
    main()