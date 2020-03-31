from colorama import Fore, Style, init


import numpy as np



class Ruler:

    def __init__(self, chain1, chain2):
        '''
        Nous donnons en premier comme attribut à l'instance les deux chaines que l'on souhaite comparer
        '''
        self.chain1 = chain1
        self.chain2 = chain2
    def red_text(text):
        init(convert = True)   #affichage en rouge dans le terminal
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    def compute(self, penalite_gap=0, penalite_remplacement=0):
        '''
        Cette méthode va attribuer à l'instance la distance minimale qui sépare les deux chaines. Par défaut, un gap ou un remplacement ont un prix identique de 1, mais si on souhaite pénaliser les gap, on peut mettre une penalité gap négative: le prix d'un gap sera alors 1 - penalite_gap. Idem pour les remplacements"
        '''
        distance = 0
        top = [] #top et bottom sont pour l'instant des listes de caractères, que
        #l'onva construire à l'envers, puis les renverser, puis reconvertir en str
        #en effet, on ne peut pas renverser une str contenant du red_text
        bottom = []
        nb_lignes = len(self.chain2)
        nb_colonnes = len(self.chain1)
        M = np.zeros((len(self.chain2)+1, len(self.chain1)+1))
        #on parcours la matrice selon les diagonales descendantes vers la gauche
        #et on construit la matrice des couts
        for n in range(nb_lignes+nb_colonnes):
            for k in range(min(n+1, nb_lignes)):
                s = 1 if self.chain2[k] == self.chain1[min(n-k, nb_colonnes-1)] else 0

                M[k+1, min(n-k, nb_colonnes-1)+1] = max(M[k, min(n-k, nb_colonnes-1)]+ s
                -penalite_remplacement, M[k+1, min(n-k, nb_colonnes-1)] \
                - penalite_gap, M[k,min(n-k, nb_colonnes-1)+1] - penalite_gap)


        coord_pointeur = [len(self.chain2), len(self.chain1)] #départ

        while coord_pointeur[0] != 0 and coord_pointeur[1] != 0: #premiere boucle

            s = 1 if self.chain2[coord_pointeur[0] -1] == \
            self.chain1[coord_pointeur[1] - 1] else 0

            if M[coord_pointeur[0]-1, coord_pointeur[1]-1] + s - penalite_remplacement ==\
             max(M[coord_pointeur[0]-1, coord_pointeur[1]] - penalite_gap,\
              M[coord_pointeur[0]-1, coord_pointeur[1] - 1] + s - penalite_remplacement,\
               M[coord_pointeur[0], coord_pointeur[1] - 1] - penalite_gap):


                if M[coord_pointeur[0]-1, coord_pointeur[1] - 1] == M[coord_pointeur[0],\
                 coord_pointeur[1]]:
                    distance += 1 - penalite_remplacement
                    top += [f"{Ruler.red_text(self.chain1[coord_pointeur[1] - 1])}"]
                    bottom += [f"{Ruler.red_text(self.chain2[coord_pointeur[0] - 1])}"]
                    coord_pointeur[0] -= 1
                    coord_pointeur[1] -= 1
                else:
                    top += [f"{self.chain1[coord_pointeur[1] - 1]}"]
                    bottom += [f"{self.chain2[coord_pointeur[0] - 1]}"]
                    coord_pointeur[0] -= 1
                    coord_pointeur[1] -= 1
            elif M[coord_pointeur[0]-1, coord_pointeur[1]] - penalite_gap ==\
             max(M[coord_pointeur[0]-1, coord_pointeur[1]], M[coord_pointeur[0]-1,\
              coord_pointeur[1] - 1] + s - penalite_remplacement, M[coord_pointeur[0],\
               coord_pointeur[1] - 1] - penalite_gap):
                coord_pointeur[0] -= 1
                distance += 1 - penalite_gap
                bottom += [f"{self.chain2[coord_pointeur[0]]}"]
                top += [f"{Ruler.red_text('=')}"]
            else:
                distance += 1 - penalite_gap
                coord_pointeur[1] -= 1
                top += [f"{self.chain1[coord_pointeur[1]]}"]
                bottom += [f"{Ruler.red_text('=')}"]

        #on arrive à la deuxième condition d'arrêt pour ajouter des espaces à la fin
        if coord_pointeur[0] == 0:
            while coord_pointeur[1] != 0:
                coord_pointeur[1] -= 1
                top += [f"{self.chain1[coord_pointeur[1]]}"]
                bottom += [f"="]
        if coord_pointeur[1] == 0:
            while coord_pointeur[0] != 0:
                coord_pointeur[0] -= 1
                top += [f"{Ruler.red_text('=')}"]
                bottom += [f"{self.chain2[coord_pointeur[0]]}"]

        top.reverse()
        bottom.reverse()

        self.distance = distance
        self.top = top
        self.bottom = bottom



    def devient_string(list):
        '''
        Tranforme une liste en string
        '''
        new_string = f""
        for a in list:
            new_string += a
        return new_string

    def report(self):
        return Ruler.devient_string(self.top), Ruler.devient_string(self.bottom)

