import socket
import ssl
import json
import sqlite3
import time


conn = sqlite3.connect("beskeder.db")
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bygning TEXT,
    sal TEXT,
    rum TEXT,
    placering TEXT,
    ip TEXT,
    maskine TEXT
)''')
conn.commit()


context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.pem")


tilladte_ip_adresser = ["10.136.128.151", "10.136.128.152"]  
forbindelser = {}  


bind_ip = "10.136.128.150"
bind_port = 10023

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((bind_ip, bind_port))
    sock.listen(5)
    print("Server lytter på port", bind_port)

    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            client_socket, addr = ssock.accept()
            ip = addr[0]

            
            if ip not in tilladte_ip_adresser:
                print("Afvist forbindelse fra (ikke whitelisted):", ip)
                client_socket.close()
                continue

            
            nu = time.time()
            sidste_tid = forbindelser.get(ip, 0)
            if nu - sidste_tid < 5:
                print(f"For mange forbindelser fra {ip} – afvist.")
                client_socket.close()
                continue
            forbindelser[ip] = nu

            print("Forbindelse fra", addr)

            try:
                data = client_socket.recv(4096).decode()
                log = json.loads(data)
                print("Modtaget:", log)

                
                c.execute('''
                    INSERT INTO logs (bygning, sal, rum, placering, ip, maskine)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (log["bygning"], log["sal"], log["rum"], log["placering"], log["ip"], log["maskine"]))
                conn.commit()
                print("Data gemt i databasen.")
            except Exception as e:
                print("Fejl:", e)
            finally:
                client_socket.close()

