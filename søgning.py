import sqlite3

conn = sqlite3.connect("beskeder.db")
c = conn.cursor()

søgefelt = input("Hvad vil du søge efter (f.eks. bygning, ip, maskine): ").strip().lower()
værdi = input("Indtast søgeværdi: ").strip()

query = f"SELECT * FROM logs WHERE {søgefelt} LIKE ?"
c.execute(query, ('%' + værdi + '%',))

resultater = c.fetchall()

for række in resultater:
    print(række)

conn.close()
