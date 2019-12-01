from collections.abc import Iterable

class Quoridor:

    noms = ()  # TODO: Initialiser cet attribut (nom des joueurs)

    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés, 
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui 
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire. 
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans 
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir 
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il 
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.

        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun mur placé sur le jeu.

        :raises QuoridorError: si joueurs n'est pas itérable.
        :raises QuoridorError: si l'itérable de joueurs en contient plus de deux.
        :raises QuoridorError: si le nombre de murs qu'un joueur peut placer est > 10, ou négatif.
        :raises QuoridorError: si la position d'un joueur est invalide.
        :raises QuoridorError: si murs n'est pas un dictionnaire lorsque présent.
        :raises QuoridorError: si le total des murs placés et plaçables n'est pas égal à 20.
        :raises QuoridorError: si la position d'un mur est invalide.
        """

        if not isinstance(joueurs, Iterable): raise QuoridorError(
            "L'argument 'joueurs' doit être un itérable")
        if len(joueurs) > 2: raise QuoridorError("Seulement 2 joueurs peuvent être spécifiés")

        
        liste_joueurs = []

        for i in range(len(joueurs)):
            if isinstance(joueurs[i], str):
                liste_joueurs.append({'nom': joueurs[i], 'murs': 10, 'position': 'adapt'})
            else:
                liste_joueurs.append(joueurs[i])
        
        bas_occ = False

        for i in range(len(liste_joueurs)):
            if liste_joueurs[i]['position'] == (5, 1):
                bas_occ = True

        for i in range(len(liste_joueurs)):
            if liste_joueurs[i]['position'] == 'adapt':
                if not bas_occ:
                    liste_joueurs[i]['position'] = (5, 1)
                    bas_occ = True
                else:
                    liste_joueurs[i]['position'] = (5, 9)
            
            valid_range = [_ for _ in range(1, 10)]
            valid_pairs = [(x, y) for x in valid_range for y in valid_range]
            if not liste_joueurs[i]['position'] in valid_pairs:
                raise QuoridorError(f"Position du joueur {i + 1} invalide")
            if not 0 <= liste_joueurs[i]['murs'] <= 10:
                raise QuoridorError(f"Le nombre de murs du joueur {i + 1} est invalide")

        self.joueurs = liste_joueurs

        # TODO: Init les murs et gérer les exceptions qui s'y rapportent (2/6) ***liste_murs


    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie. 
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """

        etat = self.état_partie()

        grid = [
            [' ' if (x - 1) % 4 != 0 else '.' for x in range(35)]
            if (y - 1) % 2 != 0 else
            [' ' for z in range(35)] for y in range(17)
        ]

        # TODO: Relier les noms
        header = (
            f'Légende: 1={etat["joueurs"][0]["nom"]}, 2={etat["joueurs"][1]["nom"]}' + 
            '\n   -----------------------------------\n'
        )
        footer = '--|-----------------------------------\n  | 1   2   3   4   5   6   7   8   9'

        # Insertion des joueurs
        pos = etat["joueurs"][0]["pos"]
        grid[pos[1] * 2 - 2][pos[0] * 4 - 3] = '1'

        pos = etat["joueurs"][1]["pos"]
        grid[pos[1] * 2 - 2][pos[0] * 4 - 3] = '2'

        # Insertion des murs horizontaux
        for i in etat["murs"]["horizontaux"]:
            y = i[1] * 2 - 3
            x = i[0] * 4 - 4
            for j in range(7):
                grid[y][x + j] = '-'

        # Insertion des murs verticaux
        for i in etat["murs"]["verticaux"]:
            y = i[1] * 2 - 2
            x = i[0] * 4 - 5
            for j in range(3):
                grid[y + j][x] = '|'

        # Transformation de la liste en ASCII art
        body = '9 |' + ''.join(grid[16]) + '|\n'
        for i in range(8, 0, -1):
            body += '  |' + ''.join(grid[i * 2 - 1]) + '|\n' + f'{i} |'+''.join(
                grid[i * 2 - 2]) + '|\n'

        tot = header + body + footer

        return tot

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la position est invalide (en dehors du damier).
        :raises QuoridorError: la position est invalide pour l'état actuel du jeu.
        """
        self.joueur = joueur
        self.position = position
        # Position antérieur des joueurs
        Anpos1 = état['joueur'][0]['pos']
        Anpos2 = état['joueur'][1]['pos']

        if joueur == 1:
            état['joueurs'][0]['pos'] = position
        if joueur == 2:
            état['joueurs'][0]['pos'] = position
        if joueur != 1 or 2:
            raise QuoridorError(f"Aucun joueur n'est associé à {joueur}")
        if position[0] < 1 or position[0] > 9:
            raise QuoridorError('Les dimensions souhaitées sont incorrectes')
        if position[1] < 1 or position[1] > 9:
            raise QuoridorError('Les dimensions souhaitées sont incorrectes')
        if Anpos[0] - position[0] != 1 or -1:
            raise QuoridorError('Le déplacement souhaité est impossible')
        if Anpos[1] - position[1] != 1 or -1:
            raise QuoridorError('Le déplacement souhaité est impossible')
        #  TODO: Error quand jeton 2 est à proximité de jeton 1
        

       
    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {'horizontaux': [...],'verticaux': [...],
            }
        }

        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée 
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est 
        associée à sa position sur le damier. Une position est représentée par un tuple 
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes x et x+1.
        """
        état = {'joueurs': liste_joueurs, 'murs': liste_murs}
        return état

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel 
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un 
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la partie est déjà terminée.
        """

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: un mur occupe déjà cette position.
        :raises QuoridorError: la position est invalide pour cette orientation.
        :raises QuoridorError: le joueur a déjà placé tous ses murs.
        """
    

class QuoridorError(Exception):
    pass
