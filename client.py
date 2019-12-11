import socket
from getpass import getpass
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(('192.168.1.122',8881))
print("\t \t********************************\t \t\n")

print ("\t \t*      Connecté au serveur     *\n ")
print("\t \t********************************\t \t")
verrouille = True
while verrouille:
    entre = getpass("Tapez le mot de passe : ") # clt ou vnd
    # On encode la saisie pour avoir un type bytes
    #entre=entre.encode()
    #entre_chiffre = hashlib.sha1(entre).hexdigest()
    my_socket.send(entre.encode())
    test = my_socket.recv(10000).decode()
    if test == "client":
        verrouille = False
        choix="1"
    elif test=="vndr":
        verrouille = False
        choix="2"
    else:
        print("Mot de passe incorrect")

print("Mot de passe accepté...")
#choix = str(input("\t      Veuillez acceder en tant que: \n\t      1)client \n\t      2)Vendeur \n\t      3)exit\n"))
my_socket.send(choix.encode())
while choix!="3":
    if (choix =="1"):#client
        donnees = str(input("Tapez votre Option : \n 1) Consulter Un produit \n 2) Acheter Un produit\n 3) exit \n"))
        my_socket.send(donnees.encode())
        while donnees != "3":
            if (donnees == "1"):
                 donne = str(input("Donnez la reference de produit :  "))
                 my_socket.send(donne.encode())
                 donne = my_socket.recv(10000).decode() #recevoir les info sur le produit à  consulter
                 print("ref Qts prix")
                 print(donne) #affichage du produit
            elif(donnees == "2" ):
                donne = str(input("saisir la reference de produit : "))
                my_socket.send(donne.encode())
                donne2 = str(input("saisir la qts a acheter :"))
                my_socket.send(donne2.encode())
                donne3 = str(input("saisir votre identifiant :"))
                my_socket.send(donne3.encode())
                donne4 = my_socket.recv(10000).decode()
                print(donne4)#affichage de la facture
            donnees = str(input("Tapez votre Option : \n 1) Consulter Un produit \n 2) Acheter Un produit\n 3)exit \n"))
            my_socket.send(donnees.encode())
    elif (choix=="2"):#vendeur
        donnees = str(input("Tapez votre Option : \n 1) Consultation  produit \n 2)consultation facture \n3)consultation de l'historique \n4)exit \n"))
        my_socket.send(donnees.encode())
        while donnees != "4":
            if (donnees == "1"):
                donne = my_socket.recv(50).decode()
                print("ref Qts prix")
                print(donne)
            if(donnees == "2" ):
                fac = my_socket.recv(100).decode()
                print("ID Somme à  payer")
                print(fac)
            if(donnees=="3"):
                nn = my_socket.recv(100).decode()
                print("ID Ref Val resultat")
                print(nn)
                
            donnees = str(input("Tapez votre Option : \n 1) Consulter  produit \n 2) consultation facture \n3) consultation de l'historique \n4) exit \n"))
            my_socket.send(donnees.encode())
    z = str(input("\t Tapez (3) si vous voulez vraiment quitter  sinon tappez n'importe quel caractere\n      "))        
    if(z=="3"):
        choix="3"
    my_socket.send(choix.encode())    
my_socket.close()

print ("Fermeture du serveur echo")


