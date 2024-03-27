import socket
import termcolor
import threading
import pickle

host, port = ('', 5566)
clients = {}
clientsIdInMatchmaking = []
matchs = {}
rooms = {}

#fonction pour gérer les commandes du terminal
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

#fonction pour créer les rooms
def createRoom(match):
    pass

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
        clientName, clientLevel, clientNbrInMatch = datas
        clientNbrInMatch = int(clientNbrInMatch)
        
        #rajout du client dans la liste clients
        
        # Trouver la première clé manquante
        newClientId = next((i for i in range(1, len(clients) + 2) if i not in clients), None)

        if newClientId is not None:
            clients[newClientId] = {'clientConn': conn, 'clientIP': address[0], 'clientLocalPort': address[1], 'clientName': clientName, 'clientLevel': int(clientLevel), 'nbrInMatch': clientNbrInMatch}
        
                    
        #verification d'un match de niveau
        if clientNbrInMatch>1: #le client est redirigé vers des salons de matchmaking
            if clientNbrInMatch in matchs: #si le nombre de personnes souhaité par le nouveau client a déjà eu des matchmakings
                if len(matchs[clientNbrInMatch][0])>0: #si le nombre de personnes souhaité par le nouveau client a des matchmaking
                    for match in matchs[clientNbrInMatch]:
                        if len(match)<clientNbrInMatch: #verification du nombre de personnes dans ce salon
                            match.append(newClientId)
                            conn.sendall(pickle.dumps(len(match)))
                            for id in match:
                                clients[id]['clientConn'].sendall(pickle.dumps(len(match)))
                            break
                else:
                    matchs[clientNbrInMatch] = [[newClientId]]
                    conn.sendall(pickle.dumps('1'))
            else:
                matchs[clientNbrInMatch] = [[newClientId]]
                conn.sendall(pickle.dumps('1'))
        else: #client non redirigé vers des salons de matchmaking
            if len(clientsIdInMatchmaking)>0:
                matchApproved = False
                for clientId in clientsIdInMatchmaking:
                    if clients[clientId]['clientLevel'] == int(clientLevel):
                        matchApproved = True
                        clientsIdInMatchmaking.remove(clientId)
                        conn.sendall(pickle.dumps(clients[clientId]['clientName']))
                        clients[clientId]['clientConn'].sendall(pickle.dumps(clientName))
                        break
                if not matchApproved:
                    clientsIdInMatchmaking.append(newClientId)
            else:
                clientsIdInMatchmaking.append(newClientId)
        
        print(f"matchs : {matchs}")
        print(f"clientsIdInMatchmaking : {clientsIdInMatchmaking}")
except:
    print(termcolor.colored("Echec du démarrage du serveur", 'red'))