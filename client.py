import socket
import ssl
import json

server_ip = "10.136.128.150"
server_port = 10023

context = ssl.create_default_context()
context.check_hostname = False  
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations("/home/klient2/server-cert.pem")

with socket.create_connection((server_ip, server_port)) as sock:
    with context.wrap_socket(sock, server_hostname=server_ip) as ssl_sock:
        print("Tilsluttet til server med SSL.")
        besked = {
            "bygning": "E",
            "sal": "2",
            "rum": "E226",
            "placering": "Guldbergsgade 29N",
            "ip": "10.136.128.151",
            "maskine": "Vm klient pc"
        }
        ssl_sock.send(json.dumps(besked).encode())
        print("Data sendt til server.")

