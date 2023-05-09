import json
import sqlite3

connection = sqlite3.connect("data/bible.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE at")
cursor.execute(
        "CREATE TABLE IF NOT EXISTS at(book VARCHAR(100) NOT NULL, chapter integer NOT NULL, verse integer NOT NULL, content TEXT NOT NULL)")

def main():
    f = open("data/AT.json")
    nt = json.load(f)
    f.close()
    for book in dict.keys(nt):
        for chapter in dict.keys(nt[book]):
            for verse in nt[book][chapter]:
                content = nt[book][chapter][verse]
                cursor.execute(f"INSERT INTO at(book,chapter,verse,content) VALUES (?,?,?,?)", (book,chapter,verse,content))
                connection.commit()

if __name__ == "__main__":
    main()