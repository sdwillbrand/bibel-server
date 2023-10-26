import json
import sqlite3

conn = sqlite3.connect("../../data/bible.db")
conn.execute('pragma journal_mode=wal')
cursor = conn.cursor()

def main():
    file_names = ["AT.json", "NT.json"]
    cursor.execute("DROP TABLE IF EXISTS book")
    cursor.execute(
                "CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY, title VARCHAR(100) NOT NULL)")
    for file_name in file_names:
        f = open(f"../data/{file_name}", "r", encoding="utf8")
        bible = json.load(f)
        f.close()
        for book in dict.keys(bible):
            cursor.execute(f"INSERT INTO book(title) VALUES ('{book}')")
            conn.commit()

if __name__ == "__main__":
    main()