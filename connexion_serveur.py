#!/usr/bin/env python
# coding: utf-8

import socket, sys
from threading import *

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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creation de la socket
       # s.bind(('', 21602)) 
        s.bind(('',listening_port)) # Bind Socket For Listen
        s.listen(max_conn) #Listening forIncoming Connections
        print("[*]Initialisation de la  Sockets .....Fait")
        print( "[*] Vous avez bien liée la sockets bravo...")
        print("[*]Le Serveur à commencé l'écoute.... [ %d ]\n" % (listening_port))
    except Exception as e:
        #execute this Block If Socket Anything Fails
        print("[*] Impossible d'initialiser la Socket")
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept() #accept Connecction from Client Browser
            data = conn.recv(buffer_size) # Receive Client Data
            threading.Thread(conn_string, (conn,data, addr)) #strat A Thread
        except KeyboardInterrupt:
            #Execute this Block if client sicked Failed
            #s.close()
            print("\n[*] Vous avez forcer l'arret de la connexion du Proxy....")
            print("[*] Passez une bonne journée!!")
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr):
# Client Browser Request Appears Here
    try:
        first_line = data.split('\n')[0]

        url = first_line.split(' ')[1]

        http_pos = url.find("://") #find the position of ://
        if (http_pos==-1):
            temp = url
        else:

            temp = url[(http_pos+3):] #get the rest of the url
        port_pos = temp.find(":") #find the Pos of the port (if any)

        webserver_pos = temp.find("/")  #Find the end of the server
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
