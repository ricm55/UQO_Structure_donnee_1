"""
* Nom: Tas d'aire
* Version: 1.0
* Date: 18/10/2021
* Auteurs: Philipe Cote, Patrick Fortier, Marc-Antoine Ricard
* 
* Description : Algorithmes de manipulation d'un tas avec d enfants
* 
* Copyright 2021
"""

import math #math.inf => represente l'infini

class Tas_d_aire:
    def __init__(self,A,d_aire):
        """
        Construit un tas
        """
        if d_aire < 2:
            raise Exception("Le tas doit obligatoirement avoir au moins 2 enfants dans un noeud")
        
        self.A = A
        self.d_aire = d_aire

        #indice du milieu du tableau
        i = int( len(A) / 2 ) - 1
        
        #Appeler entasser max depuis le milieu du tableau afin de trier le tas au complet
        while i >= 0:
            self.entasser_max(i) 
            i-=1

    def parent(self,i):
        """
        Retourne l’indice du parent du nœud A[i].
        """
        return int(i/self.d_aire - 1) if i%self.d_aire == 0 else int(i/self.d_aire)
        
    def enfants(self, i):
        """
        Retourne un range des enfants. Vide dans le cas d'une feuille
        """
        x = 1
        possede_enfant = False
       
        #Verifier si le noeud a au moins un enfant
        while(x<=self.d_aire):
            if len(self.A) > i*self.d_aire+x:
                possede_enfant = True
            x+=1
        
        if possede_enfant == False:
            return None
        return range(i*self.d_aire+1,i*self.d_aire + x)

    def entasser_max(self,i):
        """
        Trier un noeud a l'indice i
        """
        #verifier si le noeud a des enfants
        enfants = self.enfants(i)
        if enfants == None:
            return
        
        #Comparer chaque enfant et son parent afin de trouver le plus grand noeud
        max = i
        for x in enfants:
             if x < len(self.A) and self.A[x] > self.A[max]:
                 max = x
        
        #Mettre le plus grand noeud a la place du parent
        if max != i:
            self.A[i],self.A[max] = self.A[max] , self.A[i]
            #trier le nouveau max
            self.entasser_max(max)
    def extraire_max(self):
        """
        Supprime et retourne l’élément maximale dans le tas.
        """
        if len(self.A) < 1:
            raise Exception("Le tas est vide !")
        max = A[0]

        #Mettre le dernier element du tableau a la place du premier
        A[0] = A[len(A) - 1]
        A.pop()

        #Trier le premier element
        self.entasser_max(0)
        return max

    def inserer(self, key):
        """
        Insère le nouvel element dans le tas
        """
        self.A.append(-math.inf)
        self.augmenter_cle(len(self.A) - 1 , key)
    def augmenter_cle(self,i,key):
        """
        Accroît la valeur de la clé de l’élément pour lui donner
        la nouvelle valeur
        """
        #Verifier si on peut augmenter la cle
        if key < self.A[i]:
            raise Exception("La nouvelle cle est plus petite que la cle actuelle !")
        self.A[i] = key
        
        #Trier le noeud contenant la nouvel valeur
        while i >= 1 and self.A[self.parent(i)] < self.A[i]:
            self.A[i], self.A[self.parent(i)] = self.A[self.parent(i)], self.A[i]
            i = self.parent(i)

    def affiche(self):
        print(self.A)



print("******************************")
print("REPRESENTATION D'UN TAS D'AIRE 1")
print("******************************")

A = [4,1,3,2,16,9,10,14,8,7]
print("Liste initial => ", A)

#**************** Test du constructeur et entasser max ********
print("CREATION DE L'OBJET Tas_d_aire avec d=3 ...")
obj = Tas_d_aire(A,3)
print("Le tas => ",end='')
obj.affiche()
#**************************************************************
#**************** Test de parent() ****************************
print("Le parent de l'indice 5 est a l'indice ", obj.parent(5))
print("Le parent de l'indice 8 est a l'indice ", obj.parent(8))
#**************************************************************

#**************** Test de enfants() ****************************
print("Le range des enfants de l'indice 1 sont ", obj.enfants(1))
print("Le range des enfants de l'indice 2 sont ", obj.enfants(2))
#***************************************************************

#**************** Test de extraire_max() ****************************
print("Extraire le maximum => ", obj.extraire_max())
obj.affiche()
#***************************************************************

#**************** Test de augmenter_cle() ****************************
print("On veut augmenter la cle  l'indice 3 pour la valeur 6")
obj.augmenter_cle(3,6)
obj.affiche()
#*********************************************************************

#**************** Test de inserer() ****************************
print("on veut inserer la valeur 100 dans le tas")
obj.inserer(100)
obj.affiche()
#*********************************************************************

print("******************************")
print("REPRESENTATION D'UN TAS D'AIRE 2")
print("******************************")

A = [4,1,3,2,16,9,10,14,8,7,50,67,32,43,12,5,65,99,6,5,65,3,72,49,61,50]
print("Liste initial => ", A)

#**************** Test du constructeur et entasser max ********
print("CREATION DE L'OBJET Tas_d_aire avec d=5 ...")
obj = Tas_d_aire(A,5)
print("Le tas => ",end='')
obj.affiche()
#**************************************************************
#**************** Test de parent() ****************************
print("Le parent de l'indice 11 est a l'indice ", obj.parent(11))
print("Le parent de l'indice 2 est a l'indice ", obj.parent(2))
#**************************************************************

#**************** Test de enfants() ****************************
print("Le range des enfants de l'indice 1 sont ", obj.enfants(1))
print("Le range des enfants de l'indice 7 sont ", obj.enfants(7))
#***************************************************************

#**************** Test de extraire_max() ****************************
print("Extraire le maximum => ", obj.extraire_max())
obj.affiche()
print("Extraire le maximum => ", obj.extraire_max())
obj.affiche()
print("Extraire le maximum => ", obj.extraire_max())
obj.affiche()
#***************************************************************

#**************** Test de augmenter_cle() ****************************
print("On veut augmenter la cle  l'indice 3 pour la valeur 1000")
obj.augmenter_cle(3,1000)
obj.affiche()
#*********************************************************************

#**************** Test de inserer() ****************************
print("on veut inserer la valeur 100 dans le tas")
obj.inserer(100)
obj.affiche()
print("on veut inserer la valeur 122 dans le tas")
obj.inserer(122)
obj.affiche()
#*********************************************************************


print("******************************")
print("REPRESENTATION D'UN TAS D'AIRE 3")
print("******************************")

A = [4,1,3,2,16,9,10,14,8,7,50,67,32,43,12,5,65,99,6,5,65,3,72,49,61,50]
print("Liste initial => ", A)

#**************** Test du constructeur et entasser max ********
print("CREATION DE L'OBJET Tas_d_aire avec d=8 ...")
obj = Tas_d_aire(A,8)
print("Le tas => ",end='')
obj.affiche()
#**************************************************************
#**************** Test de parent() ****************************
print("Le parent de l'indice 11 est a l'indice ", obj.parent(11))
print("Le parent de l'indice 2 est a l'indice ", obj.parent(2))
#**************************************************************

#**************** Test de enfants() ****************************
print("Le range des enfants de l'indice 1 sont ", obj.enfants(1))
print("Le range des enfants de l'indice 7 sont ", obj.enfants(7))
#***************************************************************

#**************** Test de extraire_max() ****************************
print("Extraire le maximum => ", obj.extraire_max())
obj.affiche()
print("Extraire le maximum => ", obj.extraire_max())
obj.affiche()
print("Extraire le maximum => ", obj.extraire_max())
obj.affiche()
#***************************************************************

#**************** Test de augmenter_cle() ****************************
print("On veut augmenter la cle  l'indice 3 pour la valeur 1000")
obj.augmenter_cle(3,1000)
obj.affiche()
#*********************************************************************

#**************** Test de inserer() ****************************
print("on veut inserer la valeur 100 dans le tas")
obj.inserer(100)
obj.affiche()
#*********************************************************************
