import socket
import termcolor
import threading
import pickle

host, port = ('', 5566)
clients = {}
clientsInMatchmaking = []
matchs = []

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
        
        #rajout du client dans la liste clients
        
        # Trouver la première clé manquante
        nextKey = next((i for i in range(1, len(clients) + 2) if i not in clients), None)

        if nextKey is not None:
            clients[nextKey] = {'clientConn': conn, 'clientIP': address[0], 'clientLocalPort': address[1], 'clientName': clientName, 'clientLevel': int(clientLevel)}
        
        print(clientsInMatchmaking)
                    
        #verification d'un match de niveau
        if len(clientsInMatchmaking)>0:
            matchApproved = False
            for clientId in clientsInMatchmaking:
                if clients[clientId]['clientLevel'] == int(clientLevel):
                    matchApproved = True
                    clientsInMatchmaking.remove(clientId)
                    conn.sendall(pickle.dumps(clients[clientId]['clientName']))
                    clients[clientId]['clientConn'].sendall(pickle.dumps(clientName))
                    break
            if not matchApproved:
                clientsInMatchmaking.append(nextKey)
        else:
            clientsInMatchmaking.append(nextKey)
    
except:
    print(termcolor.colored("Echec du démarrage du serveur", 'red'))