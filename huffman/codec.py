from collections import Counter

class TreeBuilder:

    def recherche_plus_petite_occurence(self):
        res = []
        for key, value in self.items():
            if value[1] == 'nonused':
                res += [key]
        if res == []:
            pass
        min = res[0]
        for key in res[1:]:
            if self[key][0]<self[min][0]:
                min = key
        return min

    def __init__(self, text):
        self.text = text
        tree = {}
        occurences = Counter(self.text)
        for letter, value in occurences.items():
            tree[letter] = [value, 'nonused', 'stop', 'stop']    #0 occurences, 1 used/non used, 2-3: fils, 4 père , 5 valeur binaire
        total_occurences = sum([values for values in occurences.values()])
        max_weight_node = max([node[0] for node in tree.values()])
        while max_weight_node < total_occurences:
            min1 = TreeBuilder.recherche_plus_petite_occurence(tree)
            tree[min1][1] = 'used'            #on dit qu'il a déjà utilisé
            min2 = TreeBuilder.recherche_plus_petite_occurence(tree)
            tree[min2][1] = 'used'
            tree[min1]+= [min1 + min2]    #on dit qui va être le père
            tree[min1]+=[0]               #on dit qui est le plus léger (premier trouvé)
            tree[min2] += [min1 + min2]
            tree[min2]+=[1]               #le plus lourd
            tree[min1 + min2] = [tree[min1][0] + tree[min2][0],'nonused', min1, min2 ]   #on ajoute le père à l'arbre avec le nom de ses fils
            max_weight_node = max([node[0] for node in tree.values()])
        self.binary_tree = tree


class Codec:
    def __init__(self, text = '', code = None):
        res = TreeBuilder(text)
        self.text = res.text
        self.binary_tree = res.binary_tree
        self.code = code
    def encode(self):
        encoded = ''
        encoded_list = [] ##car aime pas trop longues trings nombres
        stop = max([node[0] for node in self.binary_tree.values()])
        for letter in self.text:
            node = letter
            reversed_code = ''
            compteur = self.binary_tree[letter][0]
            while compteur != stop:
                reversed_code += f"{self.binary_tree[node][5]}"
                node = self.binary_tree[node][4]
                compteur = self.binary_tree[node][0]
            code = reversed_code[::-1]
            encoded += f"{code}"
            encoded_list += [code]
        return encoded
    def decode(self):
        decoded = ''
        i = 0
        while i != len(self.code):
            letter = list(self.binary_tree.keys())[-1]
            while len(letter)>1:
                if self.binary_tree[self.binary_tree[letter][2]][5] == int(self.code[i]):
                    letter = self.binary_tree[letter][2]
                else:
                    letter = self.binary_tree[letter][3]
                i += 1
            decoded += f"{letter}"
        return decoded





















