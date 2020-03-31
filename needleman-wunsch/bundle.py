

from ruler import Ruler
import sys

DATASET = sys.argv[1]

with open(DATASET, 'r') as dataset:

    ligne = dataset.readlines()
    nombre_lignes = len(ligne)

    for i in range(nombre_lignes//2):
        # On utilise Ruler sur deux lignes successives.

        ruler = Ruler(ligne[2*i].strip(), ligne[2*i+1].strip())
        ruler.compute()
        top, bottom = ruler.report()

        # On affiche le résultat

        print('====== example # {} - distance = {}'.format(i+1, ruler.distance))
        print(top)
        print(bottom)
