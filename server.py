import socket
import termcolor
import threading

host, port = ('', 5566)
clients = {}
max_clients = 5

# Fonction pour gérer les commandes du terminal
def handle_commands():
    while True:
        command = input("")
        if command.strip().lower() == "downsock":
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
        
        if len(clients) < max_clients:  #Vérifie le nombre de clients
            for i in range(1, max_clients + 1):  #Regarde quel identifiant n'est pas utilisé
                if i not in clients.values():
                    clients[conn] = i
                    break
        else:
            #Ferme la plus ancienne connexion
            data = "Nombre de clients maximum atteint.".encode("utf8")
            next(iter(clients.keys())).send(data)
            clients[conn] = next(iter(clients.values()))
            next(iter(clients.keys())).close()
            del clients[next(iter(clients.keys()))]
            
        #attribution du numero au client
        clientNumber = str(list(clients.values())[-1])
        
        #reception du pseudo
        data = conn.recv(1024)
        #decodage du pseudo
        clientName = data.decode("utf8")
        print(f"Le client {clientName} vient de se connecter. Son numéro est : {clientNumber}.")
        
        #codage du clientNumber
        data = clientNumber.encode("utf8")
        #envoie des datas
        conn.send(data)
except:
    print(termcolor.colored("Echec du démarrage du serveur", 'red'))