__author__ = 'francois audet'

#import solution_v5
import ArbreRougeNoir as solution_v5

# test pred et succ
def affiche_decroissant(arbre):
    print("\nmin:", arbre.min.k, " max:", arbre.max.k)
    node = arbre.max
    while node != solution_v5.RN_arbre.nil:
        print(node.k, end=", ")
        node = node.pred
    print()

def affiche_croissant(arbre):
    print("\nmin:", arbre.min.k, " max:", arbre.max.k)
    node = arbre.min
    while node != solution_v5.RN_arbre.nil:
        print(node.k, end=", ")
        node = node.succ
    print()

a = solution_v5.RN_arbre([4,7,12,15,3,5,14,18,16,17], False)  # insertion avec affichage

print("\nrang 5: ", a.lire_rang(5).k)
print("rang 6: ", a.lire_rang(6).k)
print("rang 8: ", a.lire_rang(8).k)
print("rang 10: ", a.lire_rang(10).k)

print("rang de 3: ", a.determine_rang(3))
print("rang de 7: ", a.determine_rang(7))
print("rang de 14: ", a.determine_rang(14))
print("rang de 18: ", a.determine_rang(18))

affiche_croissant(a)
affiche_decroissant(a)

# suppression de 3, 12, 17, 18, 15, 16
a.supprimer(3)
a.affiche("\naprès Suppression de 3")

a.supprimer(12)
a.affiche("\naprès Suppression de 12")

affiche_croissant(a)
affiche_decroissant(a)

a.supprimer(17)
a.affiche("\naprès Suppression de 17")
a.supprimer(18)
a.affiche("\naprès Suppression de 18")
a.supprimer(15)
a.affiche("\naprès Suppression de 15")
a.supprimer(16)
a.affiche("\naprès Suppression de 16")

affiche_croissant(a)
affiche_decroissant(a)

b = solution_v5.RN_arbre([5,4,3,2,1,11,12,13,14,15], False)  # insertion avec affichage
