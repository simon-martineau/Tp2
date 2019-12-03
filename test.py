état = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 5]}, 
        {"nom": "automate", "murs": 3, "pos": [8, 6]}
    ], 
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]], 
        "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
    }
}

def déplacer_jeton(self, joueur, position):
      
    self.joueur = joueur
    self.position = position
    Anpos1 = état['joueur'][0]['pos']        
    Anpos2 = état['joueur'][1]['pos']

    if joueur == 1:
        état['joueurs'][0]['pos'] = position
    if joueur == 2:
        état['joueurs'][0]['pos'] = position
    if joueur != 1 or 2:
        raise QuoridorError
    if position[0] < 1 or osition[0] > 9:
        raise QuoridorError
    if position[1] < 1 or osition[1] > 9:
        raise QuoridorError
    if Anpos[0] - position[0] != 1 or -1:
        raise QuoridorError
    if Anpos[1] - position[1] != 1 or -1:
        raise QuoridorError
        #  TODO: Error quand jeton 2 est à proximité de jeton 1
    return état

if __name__ == "__main__":
    print(déplacer_jeton(1,))