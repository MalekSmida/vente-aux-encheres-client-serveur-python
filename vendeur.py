#!C:\Users\MSI\AppData\Local\Programs\Python\Python36\python.exe


import socket



my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(('192.168.1.122',8881))

print ("Connecté au serveur \n ")


while True:
    donnees = str(input("saisir une Votre Option : \n 1) Consulter Une produit \n 2) Consulter le facture d'un client \n 3)Consulter le historique des operations \n")) 
    if (donnees == "1"):
     my_socket.send(donnees.encode())
     donne = str(input("saisir le reference de produit :== > "))
     my_socket.send(donne.encode())
     donne = my_socket.recv(10000).decode()
     if (donne == "Ref Introuvable"):
         print(donne)
     else:
      donne=donne.rstrip('\n\r').split(" ")
      print("ref produit : "+donne[0]+"\nPrix :"+donne[1]+"\nQuantite :"+donne[2])
    if(donnees == "2" ):
        donnee="3"
        my_socket.send(donnee.encode())
        donne = str(input("saisir le reference de client :== > "))
        my_socket.send(donne.encode())
        donne = my_socket.recv(10000).decode()
        if (donne == "Ref Introuvable"):
         print(donne)
        else:
         donne=donne.rstrip('\n\r').split(" ")
         print("ref client : "+donne[0]+"\n Ref produit :"+donne[1]+"\n Somme a payer : "+donne[2])
    if(donnees == "3" ):
        donnee="4"
        my_socket.send(donnee.encode())
        donnes = str(my_socket.recv(10000).decode())
        print("ref client | ref produit | qts | resultat \n")
        print(donnes)
    if (donnees == "exit"):
        my_socket.send(donnees.encode())
        break     
        
my_socket.close()

print ("Fermeture du serveur echo")


