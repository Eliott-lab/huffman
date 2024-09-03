class feuille():
    def __init__(self,value:str,occurrence:int)->None:
        """
        créer la feuille
        Args:
            value (str): la lettre que cette feuille contient
            occurrence (int): le nombre d'occurrence de la lettre
        """
        self.value = value
        self.poids = occurrence
        self.path = None
        self.type = "feuille"

class Branche():
    def __init__(self,fils_gauche,fils_droit):
        """
        créer les branches
        
        Args:
            fils_gauche : le fils gauche de la branche
            fils_droit : le fils droit de la branche
        """
        self.fils_gauche = fils_gauche
        self.fils_droit = fils_droit
        self.poids = self.fils_droit.poids + self.fils_gauche.poids
        self.type = "branche"
    
    def avoir_une_lettre(self,binaries:int)->str:
        """
        retourne une lettre en le début de la suite binaire
        Args:
            binaries (int): la liste de booléens

        Returns:
            str: la lettre trouvé
        """
        if len(binaries) != 0:
            if binaries[0] == "0":
                if self.fils_gauche.type == "feuille":
                    return self.fils_gauche.value,binaries[1:]
                else:
                    return self.fils_gauche.avoir_une_lettre(binaries[1:])
            else:
                if self.fils_droit.type == "feuille":
                    return self.fils_droit.value,binaries[1:]
                else:
                    return self.fils_droit.avoir_une_lettre(binaries[1:])
    
    def lire_le_binaire(self,binaries:int)->str:
        """
        lit la suite binaire et renvoie le mot/la phrase déchiffré
        
        Args:
            binaries (int): la liste de booléens
        Returns:
            str: la phrase construite
        """
        string = ""
        while len(binaries) != 0:
            new_letter,binaries = self.avoir_une_lettre(binaries)
            string += str(new_letter)
        return string
    

    def create_path(self,str:str,dict:dict)->dict:
        """
        assigne le chemin pour chaque feuille
        
        Args:
            str (str): le chemin parcouru pour arriver jusque là depuis la racine
            dict (dict): le dictionnaire de memoisation

        Returns:
            dict: le dictionnaire contenant le chemin de toutes les lettres
        """
        
        
        if self.fils_gauche != None:
            if self.fils_gauche.type == "feuille":
                self.fils_gauche.path = str + "0"
                dict[self.fils_gauche.value] = self.fils_gauche.path
            else:
                self.fils_gauche.create_path(str+"0",dict)
        if self.fils_droit != None:
            if self.fils_droit.type == "feuille":
                self.fils_droit.path = str + "1"
                dict[self.fils_droit.value] = self.fils_droit.path
            else:
                self.fils_droit.create_path(str+"1",dict)
        return dict
    
    def afficher_arbre(self,string:str)->str:
        """

        affiche l'arbre sous forme de texte par un parcours infixe

        Args:
            string (str): le début de l'arbre sous forme de texte
        Returns:
            str: la traduction littérale de l'arbre
        """
        string += "("
        if self.fils_gauche != None:
            if self.fils_gauche.type == "feuille":
                string += self.fils_gauche.value + " = " + str(self.fils_gauche.poids)
            else:
                string = self.fils_gauche.afficher_arbre(string)
                
        string += ","
        if self.fils_droit != None:
            if self.fils_droit.type == "feuille":
                string += self.fils_droit.value + " = " + str(self.fils_droit.poids)
            else:
                string = self.fils_droit.afficher_arbre(string)
        string += ")"
        return string


def listing(sentence:str)->list[feuille]:
    """
    convertit la string en une suite de feuille

    Args:
        sentence (str): la phrase

    Returns:
        list[feuille]: notre liste de feuille
    """
    dict_of_char = {}
    for char in sentence:
        if char in dict_of_char.keys():
            dict_of_char[char] +=1
        else:
            dict_of_char[char] = 1
    list_of_char = []
    for char,occurrence in dict_of_char.items():
        list_of_char.append(feuille(char,occurrence))
    return list_of_char

def  new_list(list_of_char: list[str]) -> list[str]:
    """
    prend les deux noeud avec le poids le plus faible pour en faire un nouveau
    
    Args:
        list_of_char (list): une liste de noeud

    Returns:
        list: la nouvelle liste 
    """
    noeud_1_pos = 0
    noeud_2_pos = 1
    for noeud_pos in range(2,len(list_of_char)):
        if list_of_char[noeud_1_pos].poids > list_of_char[noeud_2_pos].poids:
            if list_of_char[noeud_pos].poids < list_of_char[noeud_1_pos].poids:
                noeud_1_pos = noeud_pos
        else:
            if list_of_char[noeud_pos].poids < list_of_char[noeud_2_pos].poids:
                noeud_2_pos = noeud_pos
    
    if noeud_1_pos < noeud_2_pos:
        noeud_1 = list_of_char.pop(noeud_1_pos)
        noeud_2 = list_of_char.pop(noeud_2_pos-1)
    else:
        noeud_2 = list_of_char.pop(noeud_2_pos)
        noeud_1 = list_of_char.pop(noeud_1_pos-1)
        
    list_of_char.append(Branche(noeud_1,noeud_2))

def text_to_tree(string:str)->Branche:
    """
        convertit la string en un arbre
    Args:
        string (str): la string d'entré

    Returns:
        Branche: l'arbre 
    """
    if len(string) != 0:
        if string[0] == "(":
            string = string[1:]
            if string[0] != "(":
                value = string[0]
                string = string[4:]
                i = 0 
                occurrence = ""
                while string[i] != ",":
                    occurrence += string[i]
                    i += 1
                occurrence = int(occurrence)
                feuille_gauche = feuille(value,occurrence)
                string = string[i+1:]
                if string[0] == "(":
                    feuille_droit,string = text_to_tree(string)
                    string = string[1:]
                    return Branche(feuille_gauche,feuille_droit),string
                else:
                    value = string[0]
                    string = string[4:]
                    i = 0 
                    occurrence = ""
                    while string[i] != ")":
                        occurrence += string[i]
                        i += 1
                    string = string[i+1:]
                    occurrence = int(occurrence)
                    feuille_droit = feuille(value,occurrence)
                    return Branche(feuille_gauche,feuille_droit),string
            else:
                
                feuille_gauche,string = text_to_tree(string)
                if string[0] == ",":
                    if string[1] == "(":
                        feuille_droit,string = text_to_tree(string[1:])
                        string = string[1:]
                        return Branche(feuille_gauche,feuille_droit),string
                    else:
                        string = string[1:]
                        value = string[0]
                        string = string[4:]
                        i = 0 
                        occurrence = ""
                        while string[i] != ")":
                            occurrence += string[i]
                            i += 1
                        string = string[i+1:]
                        occurrence = int(occurrence)
                        feuille_droit = feuille(value,occurrence)
                        return Branche(feuille_gauche,feuille_droit),string

while True:
    action = int(input("bonjour\nSi vous voulez chiffrer une phrase ou un mot, tapez 1 \nSi vous voulez déchiffrer un fichier, tapez 2: \nVous faites : "))
    if action == 1:
        #chiffrer un mot ou une phrase
        sentence = str(input("Entrez le mot ou la phrase à chiffrer,\nVous pourrez récupérer le fichier dans le \"file_deposit\" \nSi votre mot est une phrase, cherchez le fichier avec les initiales de chaque mot de votre phrase sinon, le nom de votre fichier seras le mot entrer.\n Ducoup, votre mot ou phrase est: "))
        
        list_of_char = listing(sentence)
        
        while len(list_of_char) != 1 :
            new_list(list_of_char)
            
        racine = list_of_char[0]
        
        dict = racine.create_path("",{})
        
        mot_chiffrer = ""
        for char in sentence:
            mot_chiffrer += dict[char]
        
        arbre_in_text = racine.afficher_arbre("")
        

        file = open("file_deposit\\"+str(sentence)+".txt", "w")
        
        file.write(arbre_in_text)
        
        file.write("\n")
        file.write("\n")
        
        file.write(mot_chiffrer)
        
        file.close()
        
    elif action == 2 :
        #déchiffrer un fichier
        file_path=str(input("Entrer le chemin absolu de votre fichier, verifier bien que celui-ci est formater comme le fichier exemple.\nLe chemin est: "))
        try :
            file = open(file_path)
        except :
            print("le chemin ne marche pas, réessayez")
        tree = file.readline()
        file.readline()
        binaries = file.readline()
        file.close()

        tree,string = text_to_tree(tree)
        tree.type = "racine"

        tree.create_path("",{})
        
        string = tree.lire_le_binaire(binaries)
        
        print("la traduction du fichier est : "+ string)
        

    else: 
        print("Je n'ai pas bien compris ce que vous voulez faire, veuillez réessayer :")