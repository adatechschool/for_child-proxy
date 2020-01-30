#!/usr/bin/env python
# coding: utf-8

import socket, sys
from threading import *

# choix port + quitter serveur
try:
    listening_port = int(input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:
    print ("\n[*] l'utilisateur demande l'arret du serveur")
    print ("\n[*]Vous avez quitter le serveur.....")
    sys.exit()

max_conn = 5 #maximum de connexion possible
buffer_size = 8192 # Max Socket Buffer Size

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creation de la socket
       # s.bind(('', 21602)) 
        s.bind(('',listening_port)) # lier la socket pour listen
        s.listen(max_conn) # écoute des connexions entrantes
        print("[*]Initialisation de la  Sockets .....Fait")
        print( "[*] Vous avez bien liée la sockets bravo...")
        print("[*]Le Serveur à commencé l'écoute.... [ %d ]\n" % (listening_port))
    except Exception as e:
        # execute le block si la socket échoue
        print("[*] Impossible d'initialiser la Socket")
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept() # accepter la connexion à partir du navigateur client
            data = conn.recv(buffer_size) # reçois les données clients
            threading.Thread(conn_string, (conn,data, addr)) # démarrer le Thread
        except KeyboardInterrupt:
            # exécuter ce bloc en cas d'échec du client
            # s.close()
            print("\n[*] Vous avez forcer l'arret de la connexion du Proxy....")
            print("[*] Passez une bonne journée!!")
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr):
# la demande du navigateur client apparaît ici
    try:
        first_line = data.split('\n')[0]

        url = first_line.split(' ')[1]

        http_pos = url.find("://") # trouve la position du ://
        if (http_pos==-1):
            temp = url
        else:

            temp = url[(http_pos+3):] # récupère la fin de l'url
        port_pos = temp.find(":") # trouve le Pos du port (le cas échéant)

        webserver_pos = temp.find("/")  # trouve la fin du serveur
        if  webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos==-1 or webserver_pos < port_pos):   
           port = 80        
           webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn, addr, data)
    except Exception as e:
        pass
http_pos = url.find("://") # trouver le pos de ://
if (http_pos==-1):
    temp = url
else:
    temp = url[(http_pos+3):] # obtient le reste de l'url

port_pos = temp.find(":") # trouve le port pos (le cas échéant)

# trouver la fin url serveur
webserver_pos = temp.find("/")
if webserver_pos == -1:
    webserver_pos = len(temp)

webserver = ""
port = -1
if (port_pos==-1 or webserver_pos < port_pos): 

    # port par défaut
    port = 80 
    webserver = temp[:webserver_pos] 

else: # port spécifique
    port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
    webserver = temp[:port_pos]  

def handle_client_connection(client_socket):
    raw_request = client_socket.recv(1024)
    request = HTTPRequest(raw_request)
    if request.error_code:
        print(f'Error : {request.error_code} : {request.error_message}')
    else:
        print(f'Received {request.command} {request.path}')
        try:
            response = requests.get(request.path)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print(response.text)

    client_socket.close()

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
def proxy_server(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(data)#connexion
        while 1:
            reply = s.recv(buffer_size)#espace mémoire assigné pour les infos
            if (len(reply) > 0): 
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar / 1024)#espace memoire
                dar = "%.3s" % (str(dar))#temps de rep
                dar = "%s KB" % (dar)#vitesse 
                "Print A custom Message For Request Complete"
                print ("[*] Request Done: {} => {} <=".format((str(addr[0]),str(dar))))
            else:
               break
        s.close()
        conn.close()
    except socket.error (value, message):
        s.close()
        conn.close()
        sys.exit(1)
start()
