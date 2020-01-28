#!/usr/bin/env python
# coding: utf-8
import socket, sys
from thread import *

try:
    listening_port = int(raw_input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:
    print ("\n[*] l'utilisateur demande l'arret du serveur")
    print ("\n[*]Vous avez quitter le serveur.....")
    sys.exit()
    
max_conn = 5 #maximum de connexion possible
buffer_size = 8192 # Max Socket Buffer Size

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creation de la socket
        # s.bind(('', 21602)) 
        s.bind(('',listening_port)) # Bind Socket For Listen
        s.listen(max_conn) #Listening forIncoming Connections
        print("[*]Initialisation de la  Sockets .....Fait")
        print( "[*] Vous avez bien liée la sockets bravo...")
        print("[*]Le Serveur à commencé l'écoute.... [ %d ]\n" % (listening_port))
    except Exception, e:
        #execute this Block If Socket Anything Fails
            print("[*] Impossible d'initialiser la  Socket")
            sys.exit(2)

        while 1:
            try:
                conn, addr = s.accept() #accept Connecction from Client Browser
                data = conn.recv(buffer_size) # Receive Client Data
                start_new_thread(conn_string, (conn,data, addr)) #strat A Thread
             except KeyboardInterrupt:
                #Execute this Block if client sicked Failed
                #s.close()
                print("\n[*] Vous avez forcer l'arret de la connexion du Proxy....")
                print("[*] Passez une bonne journée!!")
                sys.exit(1)
            s.close()

