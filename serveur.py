import SocketServer
import sys
import threading
import hashlib
lock = threading.Lock()
class Echo(SocketServer.BaseRequestHandler):
    def handle(self):
     global lock         
     while True:
        print ("Connexion de ", self.client_address,n)
        mot_de_passe_clt = b"clt"
        mot_de_passe_chiffre_clt = hashlib.sha1(mot_de_passe_clt).hexdigest()
        mot_de_passe_v = b"vnd"
        mot_de_passe_chiffre_v = hashlib.sha1(mot_de_passe_v).hexdigest()
        test="error"
        while test=="error":
            print("done")
            mp= self.request.recv(8192).decode()
            mp=mp.encode()
            mp1=hashlib.sha1(mp).hexdigest()
            if mp1== mot_de_passe_chiffre_clt:
                test="client"
                self.request.send(test.encode())
            elif  mp1==mot_de_passe_chiffre_v:
                test="vndr"
                self.request.send(test.encode())
            else:
                self.request.send(test.encode())
        donneesRecues = self.request.recv(8192).decode()
        print ("Données Recues : ", donneesRecues)
        while(donneesRecues!="3"):
            if ( donneesRecues == "1"):#client
                print("Client connecté")
                choix=self.request.recv(8192).decode()
                while(choix !="3"):
                    if (choix=="1"):
                        print("Consultation de produit")
                        ref=self.request.recv(8192).decode()
                        f = open("bien.txt","r")
                        donnes = f.readlines()
                        max=0
                        for ligne in donnes:
                            donne=ligne.rstrip('\n\r').split(" ")
                            if (max<int(donne[0])):
                                max=int(donne[0])
                            if (donne[0] == ref):
                                self.request.send(ligne.encode())
                        if(max<int(ref)):
                            ss="Ref Introuvable"
                            self.request.send(ss.encode())
                        f.close()
                    if ( choix == "2"):#miseajour
                        print("Achat")
                        lock.acquire()
                        ref=self.request.recv(8192).decode()
                        qt=self.request.recv(8192).decode()
                        ident=self.request.recv(8192).decode()
                        f = open("bien.txt","r")
                        donnes = f.readlines()
                        max=0
                        for ligne in donnes:
                            if(max<int(ligne[0])):
                                max=int(ligne[0])
                            donne=ligne.rstrip('\n\r').split(" ")
                            if (donne[0] == ref):
                                c=str(ref)+" "+str(int(donne[1]))+" "+str(int(donne[2]))+"\n"
                                if (int(donne[2]) >= int(qt)):
                                    donne[2]=str(int(donne[2])-int(qt))
                                    f2 = open("histo.txt","a")
                                    ch=str(ident)+" "+str(ref)+" "+str(qt)+" "+"succes"+"\n"
                                    f2.write(ch)
                                    f2.close()
                                    fs = open("bien.txt","r")
                                    lines=fs.readlines()
                                    fs.close()
                                    fs = open("bien.txt","w")
                                    for line in lines:
                                        if line!=c :
                                            fs.write(line)
                                    fs.close()
                                    f3 = open("bien.txt","a")
                                    ch1=str(ref)+" "+str(int(donne[1]))+" "+str(int(donne[2]))+"\n"
                                    f3.write(ch1)
                                    f3.close()
                                    f_facture=open("facture.txt","a")
                                    ch=str(ident)+" "+str(int(donne[1])*int (qt))+"\n"
                                    f_facture.write(ch)
                                    f_facture.close()
                                    self.request.send(ch.encode())
                                else:
                                    f2 = open("histo.txt","a")
                                    ch=str(ident)+" "+str(ref)+" "+str(qt)+" "+"echec"+"\n"
                                    f2.write(ch)
                                    f2.close()
                                    ch="Quantité insuffisante"
                                    self.request.send(ch.encode())
                                    
                        if(max<int(ref)):
                            ch="produit non trouvé"
                            self.request.send(ch.encode())
                            
                        lock.release()
                    choix=self.request.recv(8192).decode()                
            if ( donneesRecues == "2"):#vendeur
                print("Vendeur connecté")
                choix=self.request.recv(8192).decode()
                while(choix !="4"):
                    if (choix=="1"):#consultation produit
                        lock.acquire()
                        f = open("bien.txt","r")
                        donnes = f.read()
                        self.request.send(donnes.encode())
                        print(donnes)
                        f.close()
                        lock.release()
                    if (choix=="2"):#consultation facture
                        lock.acquire()
                        f2 = open("facture.txt","r") 
                        fac = f2.read()
                        self.request.send(fac.encode())
                        f2.close()
                        lock.release()
                    if (choix=="3"):#consultation historique
                        lock.acquire()
                        f3= open("histo.txt","r")
                        h = f3.read()
                        self.request.send(h.encode())
                        f3.close()
                        lock.release()
                    choix=self.request.recv(8192).decode()
                    print(choix)
            donneesRecues = self.request.recv(8192).decode()
            print ("Données Recues : ", donneesRecues)                         

        #lock.release()
        self.request.close()
        
        print ("Deconnexion de ", self.client_address)


sys.stderr=sys.stdout
n=0
while True:
    
    print ("Creation du serveur echo Multi-thread") 
    serveur = SocketServer.ThreadingTCPServer(('192.168.1.122',8881), Echo)
    print ("Attente de connexion client")
    serveur.serve_forever()
    
os.system("pause")
