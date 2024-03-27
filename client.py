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
    nbrInMatch = input("Entrez le nombre de personnes avec qui vous voulez matcher :\n")
    #codage des datas
    datas = [clientName, clientLevel, nbrInMatch]
    datas = pickle.dumps(datas)
    #envoie des datas
    server.sendall(datas)
    
    matchmakingFinish = False
    
    while not matchmakingFinish:
        datas = server.recv(1024)
        datas = pickle.loads(datas)
        try:
            if int(datas) == int(nbrInMatch):
                matchmakingFinish = True
            print(f"Matchmaking..... {datas}/{nbrInMatch}", end='\r')
        except:
            print("problème")
    
except ConnectionRefusedError:
    print(termcolor.colored("Le client n'a pas pu se connecter", 'red'))
finally:
    server.close()