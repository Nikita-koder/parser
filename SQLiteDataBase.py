import sqlite3


def executeSqlDataBase(data):
    conn = sqlite3.connect(r"PlayToEarnDB.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS games(
                            id INT NOT NULL,
                            imgUrl TEXT,
                            gameName TEXT,
                            status TEXT
                            
                      );
                   """)
    conn.commit()
    cursor.executemany("INSERT INTO games VALUES (?,?,?,?);", data)
    conn.commit()