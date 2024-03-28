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
        
        print("a")
        #verification d'un match de niveau
        if clientNbrInMatch>1: #le client est redirigé vers des salons de matchmaking
            print("b")
            if clientNbrInMatch in matchs: #si le nombre de personnes souhaité par le nouveau client a déjà eu des matchmakings
                print("c")
                if len(matchs[clientNbrInMatch])>0: #si le nombre de personnes souhaité par le nouveau client a des matchmaking
                    print("d")
                    for match in range(len(matchs[clientNbrInMatch])):
                        if len(matchs[clientNbrInMatch][match])<clientNbrInMatch: #verification du nombre de personnes dans ce salon
                            matchs[clientNbrInMatch][match].append(newClientId)
                            conn.sendall(pickle.dumps(len(matchs[clientNbrInMatch][match])))
                            for id in matchs[clientNbrInMatch][match]:
                                clients[id]['clientConn'].sendall(pickle.dumps(len(matchs[clientNbrInMatch][match])))
                            if len(matchs[clientNbrInMatch][match])==clientNbrInMatch: #verification salon de matchmaking complet
                                
                                #création de la room
                                newRoomId = next((i for i in range(1, len(rooms) + 2) if i not in rooms), None) #id de room disponible
                                if newRoomId is not None:
                                    rooms[newRoomId] = matchs[clientNbrInMatch][match]
                                
                                #suppression du matchmaking dans matchs
                                matchs[clientNbrInMatch].pop(match)
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
        print(f"rooms : {rooms}")
except:
    print(termcolor.colored("Echec du démarrage du serveur", 'red'))