import socket
import termcolor
import threading
import pickle

host, port = ('', 5566)
clients = []

# Fonction pour gérer les commandes du terminal
def handle_commands():
    while True:
        command = input("")
        if command.strip().lower() == "closesock":
            #Fermeture  du serveur
            server.close()
            print(termcolor.colored("Serveur arrêté", 'red'))
            break

# Création du thread pour gérer les commandes du terminal
command_thread = threading.Thread(target=handle_commands, daemon=True)
command_thread.start() 

#creation du serveur
server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#lancement du serveur
try:
    server.bind((host, port))
    print(termcolor.colored("Serveur démarré", 'green'))
    
    while True:
        server.listen() #serveur en ecoute
        conn, address = server.accept() #connexion etablie
        
        #reception du pseudo
        datas = conn.recv(1024)
        #decodage du pseudo
        datas = pickle.loads(datas)
        clientName, clientLevel = datas
        
        #verification d'un match de niveau
        for client in clients:
            if client['clientLevel'] == int(clientLevel):
                conn.sendall(pickle.dumps(client['clientName']))
                client['clientConn'].sendall(pickle.dumps(clientName))
        
        #rajout du client dans la liste clients
        clients.append({'clientConn': conn, 'clientIP': address[0], 'clientLocalPort': address[1], 'clientName': clientName, 'clientLevel': int(clientLevel)})
except:
    print(termcolor.colored("Echec du démarrage du serveur", 'red'))