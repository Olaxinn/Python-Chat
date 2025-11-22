import sqlite3

con = sqlite3.connect('messages.db')
cur = con.cursor()
cur.execute("DELETE FROM messages")  # Tablodaki tüm satırları siler
con.commit()
con.close()