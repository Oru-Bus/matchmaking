import socket
import termcolor


host, port = ('127.0.0.1', 5566)

server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connexion au serveur
try:
    server.connect((host, port))
    print(termcolor.colored("Le client s'est connecté", 'green'))
    
    clientName = input("Entrez votre pseudo :\n")
    #codage des datas
    data = clientName.encode("utf8")
    #envoie des datas
    server.sendall(data)
    
    #reception du nbClient
    data = server.recv(1024)
    #decodage du nbClient
    nbClient = data.decode("utf8")
    print(f"Votre numéro client est le suivant : {nbClient}.")
    
    message = server.recv(1024).decode("utf8")
    if message == "Nombre de clients maximum atteint.":
        print("Le nombre maximal de clients est atteint. La connexion se ferme.")
    
except ConnectionRefusedError:
    print(termcolor.colored("Le client n'a pas pu se connecter", 'red'))
finally:
    server.close()