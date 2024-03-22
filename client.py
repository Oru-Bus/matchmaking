import socket
import termcolor
import pickle


host, port = ('127.0.0.1', 5566)

server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connexion au serveur
try:
    server.connect((host, port))
    print(termcolor.colored("Le client s'est connecté", 'green'))
    
    clientName = input("Entrez votre pseudo :\n")
    clientLevel = input("Entrez votre niveau :\n")
    #codage des datas
    datas = [clientName, clientLevel]
    datas = pickle.dumps(datas)
    #envoie des datas
    server.sendall(datas)
    
    datas = server.recv(1024)
    matchName = pickle.loads(datas)
    print(f"Vous avez matché avec {matchName} !")
    
except ConnectionRefusedError:
    print(termcolor.colored("Le client n'a pas pu se connecter", 'red'))
finally:
    server.close()