"""
* Nom: Arbre Rouge-Noir
* Version: 1.0
* Date: 06/12/2021
* Auteurs: Philipe Cote, Patrick Fortier, Marc-Antoine Ricard
* 
* Nom d'équipe: Les petits Pouttes Pouttes
* 
* Description : Implementation de la  structure de donnée Arbre Rouge-Noir
* 
* @Copyright 2021
"""

class Noeud:
    def __init__(self,k,c,p,g,d,t,pred,succ):
        self.k = k
        self.c = c
        self.p = p
        self.g = g
        self.d = d
        self.t = t
        self.pred = pred
        self.succ = succ
    def __str__(self):
        x = lambda n:("Vide" if n == None else n.k)
        
        return f"Objet Noeud: \n\
                Clé: {self.k}\n\
                Couleur: {self.c}\n\
                Parent: {x(self.p)}\n\
                Gauche: {x(self.g)}\n\
                Droite: {x(self.d)}\n\
                Taille: {self.t}\n\
                Prédécesseur: {x(self.pred)}\n\
                Successeur: {x(self.succ)}\n"

NIL = Noeud("NIL","NOIR",None,None,None,0,None,None)
class RN_arbre:
    nil = NIL
    def __init__(self,tab,modeAffichage):
        
        # Mode si True permettant d'afficher des informations supplementaires
        # durant l'execution du programme
        self.modeAffichage = modeAffichage
        
        self.nil = NIL
        self.racine = NIL
        self.max = NIL
        self.min = NIL

        #Inserer chaque element du tableau dans l'arbre
        for k in tab:
            self.arbre_inserer(k)
    
    def trouve_noeud(self,i,racine=None):
        """
        Retourne un noeud de l’arbre dont la clé vaut i
        """
        if self.modeAffichage:
            print("Recherche d'un noeud en cours...")
        #Si le sous-arbre n'est pas defini, rechercher a partir de la racine
        if racine == None:
            racine = self.racine

        #Retourner la racine si elle est recherche
        if racine == self.nil or i == racine.k:
            return racine
        
        #Definir le coté de recherche du noeud
        if i <racine.k:
            return self.trouve_noeud(i,racine.g)
        else:
            return self.trouve_noeud(i,racine.d)
    
    def arbre_inserer(self,i):
        """
        Crée un noeud qui a i comme clé, puis l’insère dans l’arbre. 
        Si i est un noeud, celui-ci est inséré directement.
        """
        
        #Creer un noeud avec la clé donné si besoins
        if isinstance(i,Noeud):
            z = i
        else:
            z = Noeud(i,None,None,None,None,0,self.nil,self.nil)

        if self.modeAffichage:
            print(f"Inserer le noeud {z} dans l'arbre...")

        #Debut de l'insertion du noeud
        y = self.nil
        x = self.racine

        #determiner de quel coté inserer le noeud
        while x != self.nil:
            y = x
            if z.k <x.k:
                x = x.g
            else:
                x = x.d
        
        #definir le pere du nouveau noeud
        z.p = y

        #initialiser les attributs si on insere le premier noeud
        if y == self.nil:
            self.racine = z
            self.max = z
            self.min = z
        
        # Determiner vers quel cote le nouveau noeud se trouve par rapport au pere
        # et ajouter les predecesseurs et successeurs
        elif z.k < y.k:
            y.g = z
            self.ajout_pred_succ(y,z)
        else:
            y.d = z
            self.ajout_pred_succ(y,z)
        
        #Mettre propriétés du nouveau noeud par defaut
        z.g = self.nil
        z.d = self.nil
        z.c = "ROUGE"
        z.t = 1
        
        #Mettre la taille a jour pour tous les noeuds au dessus
        updateTaille = z.p
        while updateTaille != self.nil:
            updateTaille.t+=1
            updateTaille = updateTaille.p

        #Correction s'il y a une violation de propriétés
        self.inserer_correction_rn(z)

        #Update du minimum et maximum dans l'arbre
        if z.k > self.max.k:
            self.max = z
        if z.k < self.min.k:
            self.min = z
        
    def supprimer(self,i):
        """
        Supprime l’élément dont la clé est i.
        """
        
        #Trouver le noeud a supprimer
        z = self.trouve_noeud(i)
        if z == self.nil:
            #Le noeud a supprimer n'existe pas
            if self.modeAffichage:
                print(f"Le noeud avec la clé {i} n'existe pas dans l'arbre...")
            return self.nil
        
        if self.modeAffichage:
            print(f"Suppression du noeud {z} dans l'arbre...")

        #Update la taille de tous les noeuds au-dessus
        updateTaille = z
        while updateTaille != self.nil:
            updateTaille.t-=1
            updateTaille = updateTaille.p
        
        #Verifie si le minimum est supprime et le modifier si besoins
        if z == self.min:
            if z.d != self.nil:
                self.min = z.d
            elif z.p == self.racine:
                self.min = self.racine
            else:
                self.min = z.p
        
        #Verifie si le maximum est supprime et le modifier si besoins
        if z == self.max:
            if z.p != self.nil:
                self.max = z.p
            else:
                self.max = z.g
        
        #Modifier les predecesseurs et successeurs au besoins
        self.supprime_pred_suc(z)

        #Debuter l'algorithme du supprimer
        y = z
        y_original_couleur = y.c # Memoriser la couleur de y
        
        #Definir de quel cote transplanter le sous-arbre
        if z.g == self.nil:
            x = z.d
            self.transplante_rn(z,z.d)
        elif z.d == self.nil:
            x = z.g
            self.transplante_rn(z,z.g)
        
        #Les 2 enfants ne sont pas NIL
        else:
            y = self.arbre_minimum(z.d)
            y_original_couleur = y.c #y devient le successeur de z
            x = y.d

            # Si y est un enfant de z
            if y.p == z:
                x.p = y
            else:
                self.transplante_rn(y,y.d)
                y.d = z.d
                y.d.p = y

            self.transplante_rn(z,y)
            y.g = z.g
            y.g.p = y
            y.c = z.c # y prend la couleur de z

        if y_original_couleur == "NOIR":
            #Apporter la correction a l'arbre
            self.supprimer_correction_rn(x) 
        
    def lire_rang(self,i,x=None):
        """
        Retourne l’élément de rang i de l’arbre
        """
        if self.modeAffichage:
            print(f"Lecture du rang du noeud avec la clé {i} en cours...")

        #Si pas précisé, lire le rang depuis la racine
        if x == None:
            x = self.racine

        r = x.g.t + 1

        #Le rang est trouvé
        if i == r:
            return x

        #Definir de quel coté parcourir l'arbre
        elif i <r:
            return self.lire_rang(i, x.g)
        else:
            return self.lire_rang(i-r, x.d)
        
    def determine_rang(self,x):
        """
        Retourne la position du noeud x dans l’ordre linéaire tel 
        que déterminé par un parcours inFixe de l’arbre.
        """
        if self.modeAffichage:
            print(f"Determiner le rang du noeud en cours...")
        #Si l'utilisateur donne une clé, trouvé le noeud
        if isinstance(x,Noeud) == False:
            x = self.trouve_noeud(x)

        #Calculer le rang
        r = x.g.t + 1
        y = x

        #Decendre dans l'arbre jusqu'a temps que le rang soie trouv
        while y != self.racine:
            if y == y.p.d:
                r = r + y.p.g.t + 1
            y = y.p
        return r
        
    def ajout_pred_succ(self,y,z):
        """
        Fonction qui rétablit les propriétés pred et succ
        suite à l’insertion de x dans l’arbre.
        """
        if self.modeAffichage:
            print(f"Modification des successeurs et predecesseurs pour l'insertion du noeud en cours...")
        #Si le noeud est a gauche
        if z == y.g:
            if y.pred != self.nil:
                y.pred.succ = z
            z.pred = y.pred
            z.succ = y
            y.pred = z
        #Si le noeud est a droite
        else:
            if y.succ != self.nil:
                y.succ.pred = z
            z.succ = y.succ
            y.succ = z
            z.pred = y
        
    def supprime_pred_suc(self,z):
        """
        Fonction qui rétablit les propriétés pred et succ
        suite à la suppression de z de l’arbre.
        """
        if self.modeAffichage:
            print(f"Modification des successeurs et predecesseurs pour la suppression du noeud en cours...")
        z.pred.succ = z.succ # Le predecesseur de la cle supprime herite du successeur de celle-ci
        z.succ.pred = z.pred # Le successeur de la cle supprime herite du prodecesseur de celle-ci

    def inserer_correction_rn(self,z):
        """
        Apporte les corrections a l'arbre lorsqu'un nouveau noeud se fait inserer
        """
        if self.modeAffichage:
            print(f"Apporter la correction a l'insertion du nouveau noeud en cours...")
        
        while z.p.c == "ROUGE":
            if z.p == z.p.p.g:
                y = z.p.p.d # recuperer l'oncle de z
                
                #Case 1: l'oncle de z est rouge
                #on doit recolorier le parent, grand-parent et oncle
                if y.c == "ROUGE":
                    z.p.c = "NOIR"
                    y.c = "NOIR"
                    z.p.p.c = "ROUGE"
                    z = z.p.p

                #Case 2: l'oncle de z est noir (triangle)
                else:
                    if z == z.p.d:
                        z = z.p
                        self.rotation_gauche(z)    
                    
                    #Case 3: l'oncle est noir (en ligne)
                    z.p.c = "NOIR"
                    z.p.p.c = "ROUGE"
                    self.rotation_droite(z.p.p) # sort de la boucle puisque z.p deviens noir
            
            #repeter les memes interractions en changeant de cote
            else:
                y = z.p.p.g # recuperer l'oncle de z
                
                #Case 1: l'oncle de z est rouge
                #on doit recolorier le parent, grand-parent et oncle
                if y.c == "ROUGE":
                    z.p.c = "NOIR"
                    y.c = "NOIR"
                    z.p.p.c = "ROUGE"
                    z = z.p.p

                #Case 2: l'oncle de z est noir (triangle)
                else:
                    if z == z.p.g:
                        z = z.p
                        self.rotation_droite(z)
                            
                    #Case 3: l'oncle est noir (en ligne)
                    z.p.c = "NOIR"
                    z.p.p.c = "ROUGE"
                    self.rotation_gauche(z.p.p) # sort de la boucle puisque z.p deviens noir
        self.racine.c = "NOIR"
        
    def supprimer_correction_rn(self,x):
        """
        Apporte les corrections a l'arbre lorsqu'un noeud se fait supprimé
        """
        if self.modeAffichage:
            print(f"Apporter la correction a la suppression du nouveau noeud en cours...")
        
        while x != self.racine and x.c == "NOIR":
            if x == x.p.g:
                w = x.p.d

                # Cas 1: le frere de x est rouge
                if w.c == "ROUGE":
                    
                    w.c == "NOIR"
                    x.p.c = "ROUGE"
                    self.rotation_gauche(x.p)
                    w = x.p.d
                
                #w est un nil
                #Cas 2: Le frere de x est noir et les 2 enfants de w sont noirs
                if w.g.c == "NOIR" and w.d.c == "NOIR":
                    w.c = "ROUGE"
                    x = x.p

                #Cas 3: Le frère de x, est noir, w.gauche est rouge et w.droite est noir
                else:
                    if w.d.c == "NOIR":
                        w.g.c = "NOIR"
                        w.c = "ROUGE"
                        self.rotation_droite(w)
                        w = x.p.d    
                    #Cas 4: Le frère de x, est noir et w.droite est rouge.
                    w.c = x.p.c
                    x.p.c = "NOIR"
                    w.d.c = "NOIR"
                    self.rotation_gauche(x.p)
                    x = self.racine
            else:
                w = x.p.g

                # Cas 1: le frere de x est rouge
                if w.c == "ROUGE":
                    w.c == "NOIR"
                    x.p.c = "ROUGE"
                    self.rotation_droite(x.p)
                    w = x.p.g
                
                #Cas 2: Le frere de x est noir et les 2 enfants de w sont noirs
                if w.d.c == "NOIR" and w.g.c == "NOIR":
                    w.c = "ROUGE"
                    x = x.p

                #Cas 3: Le frère de x, est noir, w.gauche est rouge et w.droite est noir
                else:
                    if w.g.c == "NOIR":
                        w.d.c = "NOIR"
                        w.c = "ROUGE"
                        self.rotation_gauche(w)
                        w = x.p.g    
                    #Cas 4: Le frère de x, est noir et w.droite est rouge.
                    w.c = x.p.c
                    x.p.c = "NOIR"
                    w.g.c = "NOIR"
                    self.rotation_droite(x.p)
                    x = self.racine
        x.c = "NOIR"
    def transplante_rn(self,u,v):
        """
        Transplante un sous-arbre a l'endroit donné
        """
        if self.modeAffichage:
            print(f"Transplante du sous-arbre en cours...")
        if u.p == self.nil: #Sentinelle NIL
            self.racine = v
        elif u == u.p.g:
            u.p.g = v
        else:
            u.p.d = v
        v.p = u.p
    def rotation_gauche(self, x):
        """
        Effectuer une rotation d'un noeud vers la gauche
        """
        if self.modeAffichage:
            print(f"Rotation gauche en cours...")
        y = x.d # initialize y
        x.d = y.g # sous-arbre de y devient sous-arbre droit de x
        if y.g != self.nil:
            y.g.p = x
        y.p = x.p # relie parent de x a y
        if x.p == self.nil: # x etait la racine
            self.racine = y # y devient la nouvelle racine
        elif x == x.p.g: # Modifie le parent de x
            x.p.g = y
        else:
            x.p.d = y
        y.g = x # Place x a gauche de y
        x.p = y # y devient le parent x

        #Modifier la taille des noeuds affectés
        y.t = x.t
        x.t = x.g.t + x.d.t + 1
    def rotation_droite(self,x):
        """
        Effectuer une rotation d'un noeud vers la droite
        """
        if self.modeAffichage:
            print(f"Rotation droite en cours...")
        y = x.g # initialize y
        x.g = y.d # sous-arbre de y devient sous-arbre droit de x
        if y.d != self.nil:
            y.d.p = x
        y.p = x.p # relie parent de x a y
        if x.p == self.nil: # x etait la racine
            self.racine = y # y devient la nouvelle racine
        elif x == x.p.d: # Modifie le parent de x
            x.p.d = y
        else:
            x.p.g = y
        y.d = x # Place x a gauche de y
        x.p = y # y devient le parent x
        
        #Modifier la taille des noeuds affectés
        y.t = x.t
        x.t = x.d.t + x.g.t + 1
    def arbre_minimum(self,x):
        """
        Algorithme permettant de trouver le minimum d'un sous-arbre ou un arbre donné
        """
        if self.modeAffichage:
            print(f"Calcule du minimum du sous-arbre en cours...")
        while x.g != self.nil:
            x = x.g
        return x
    
    def affiche(self,chaine=None,x=None):
        """
        AfFiche les noeuds de l’arbre dans un parcours infixe
        """
        #Afficher une chaine que l'utilisateur souhaite
        if chaine != None:
            print(chaine)
        
        if x == None:
            x = self.racine
            #L'arbre est vide
            if x == self.nil:
                print("Arbre vide")
                return
        if x != self.nil:
            self.affiche(None,x.g)
            print(x)
            self.affiche(None,x.d)
        
if __name__ == "__main__":
    #tab = [22,11,34,12,4]
    #tab = [22,11,34,12]
    #tab = [15,6,18,3,7,17,20,2,4,13,9]
    #tab = [26,17,41,14,21,30,47,10,16,19,21,28,38,7,12,14,20,35,39,3]
    tab = [6,5,7,2,5,8]
    obj = RN_arbre(tab,False)
    #n = obj.lire_rang(obj.racine.d,2)
    #print(n)
    #n = obj.trouve_noeud(47)
    #t = obj.determine_rang(n)
    #print(t)
    obj.supprimer(20)
    obj.affiche()
    #obj.supprimer(34)
    #obj.supprimer(22)
    #obj.supprimer(19)
    #obj.affiche()
    #obj.supprimer(4)
    #obj.supprimer(11)
    
    #Test minimum
    #obj.supprimer(11)
    #obj.supprimer(12)
    #obj.supprimer(22)
    #obj.supprimer(34)
    
    #print(obj.minimum)

    #Test maximum
    #obj.supprimer(34)
    #obj.supprimer(22)
    #obj.supprimer(12)
    #obj.supprimer(11)
    #obj.supprimer(12)
    #obj.supprimer(11)
    
    #print(obj.maximum)
    
    #minimum = obj.maximum
    #response = obj.trouve_noeud(65)
    #response = obj.trouve_noeud(66)

    #response = obj.arbre_minimum(obj.racine)
    
    #obj.affiche()
    #print(response)
    #print(f"maximum: {maximum}")
    