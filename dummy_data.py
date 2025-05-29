import sqlite3


conn = sqlite3.connect("beskeder.db")
c = conn.cursor()


ekstra_data = [
    ("F", "3", "F302", "Lyngbyvej 100", "10.136.128.160", "printer1"),
    ("G", "1", "G102", "Borups Allé 12", "10.136.128.161", "PC-Lab 2"),
    ("H", "2", "H201", "Nørrebrogade 88", "10.136.128.162", "PC-Lab 3"),
]


for entry in ekstra_data:
    c.execute('''
        INSERT INTO logs (bygning, sal, rum, placering, ip, maskine)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', entry)

conn.commit()
conn.close()

print("Fiktive data er indsat i databasen.")
