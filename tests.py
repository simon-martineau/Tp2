import unittest
from quoridor import Quoridor, QuoridorError


class TestQuoridorInit(unittest.TestCase):

    def test_init_with_strings(self):
        partie = Quoridor(['Simon', 'Robot'])

        self.assertEqual(
            partie.joueurs,
            [
                {'nom': 'Simon', 'murs': 10, 'pos': (5, 1)},
                {'nom': 'Robot', 'murs': 10, 'pos': (5, 9)},
            ],
        )

        self.assertEqual(
            partie.murs,
            {'horizontaux': [], 'verticaux': []}
        )

    def test_init_with_state(self):
        # Initiation d'une partie avec une liste de dictionnaires
        partie = Quoridor(
            [{"nom": "idul", "murs": 7, "pos": [5, 5]}, {
                "nom": "automate", "murs": 3, "pos": [8, 6]}],
            murs={
                "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
            }
        )

        self.assertEqual(
            partie.joueurs,
            [
                {'nom': 'idul', 'murs': 7, 'pos': [5, 5]},
                {'nom': 'automate', 'murs': 3, 'pos': [8, 6]},
            ]
        )

        self.assertEqual(
            partie.murs,
            {
                "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
            }
        )

    def test_init_exceptions(self):
        def not_iterable():
            return Quoridor(5)

        def one_player():
            return Quoridor(['Simon'])

        def three_players():
            return Quoridor(['Simon', 'Raph', 'JS'])

        def murs_negatifs():
            return Quoridor(
                [{'nom': 'Simon', 'murs': -1, 'pos': (5, 1)}, 'Robot'])

        def murs_plus_de_10():
            return Quoridor(
                [{'nom': 'Simon', 'murs': 11, 'pos': (5, 1)}, 'Robot'])

        def position_hors_limites():
            return Quoridor(
                [{'nom': 'Simon', 'murs': 10, 'pos': (10, 1)}, 'Robot'])

        def murs_pas_un_dictionnaire():
            return Quoridor(['Simon', 'Robot'], murs='foo')

        def murs_total_erroné():
            return Quoridor(['Simon', 'Robot'], murs={
                'horizontaux': [(4, 4)], 'verticaux': []})

        def pos_mur_erroné():
            return Quoridor(
                [{'nom': 'Simon', 'murs': 10, 'pos': (10, 1)}, 'Robot'],
                murs={
                    'horizontaux': [(3, 5)],
                    'verticaux': [(4, 4)]
                }
            )

        fn_list = [
            not_iterable, one_player, three_players, murs_negatifs,
            murs_plus_de_10, position_hors_limites, murs_pas_un_dictionnaire,
            murs_total_erroné, pos_mur_erroné
        ]

        for fn in fn_list:
            with self.subTest():
                self.assertRaises(QuoridorError, fn)


class TestQuoridorMethods(unittest.TestCase):

    def setUp(self):
        self.partie = Quoridor(
            [{"nom": "idul", "murs": 7, "pos": [5, 5]}, {
                "nom": "automate", "murs": 3, "pos": [8, 6]}],
            murs={
                "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
            }
        )

    def test_état_partie(self):
        état = self.partie.état_partie()
        self.assertEqual(
            état,
            {
                "joueurs": [
                    {"nom": "idul", "murs": 7, "pos": [5, 5]},
                    {"nom": "automate", "murs": 3, "pos": [8, 6]}
                ],
                "murs": {
                    "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                    "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
                }
            }
        )

    # Test pour les erreurs dans la facontion placer mur
    def test_placer_mur_exceptions(self):

        def joueur_erroné_0():
            self.partie.placer_mur(joueur=0, position=(
                4, 5), orientation='horizontal')

        def joueur_erroné_3():
            self.partie.placer_mur(joueur=3, position=(
                4, 5), orientation='horizontal')

        def mur_occupe_position():
            self.partie.placer_mur(joueur=1, position=(
                4, 4), orientation='horizontal')

        def position_mur_invalide():
            self.partie.placer_mur(joueur=1, position=(
                11, 11), orientation='horizontal')

        fn_list = [joueur_erroné_0, joueur_erroné_3,
                   mur_occupe_position, position_mur_invalide]
        for fn in fn_list:
            with self.subTest():
                self.assertRaises(QuoridorError, fn)

    #Test pour le fonctionnement de placer mur
    def test_placer_mur_logique(self):
        partie = self.partie
        partie.placer_mur(1, (2, 2), 'vertical')

        self.assertEqual(
            {
                "joueurs": [
                    {"nom": "idul", "murs": 7, "pos": [5, 5]},
                    {"nom": "automate", "murs": 3, "pos": [8, 6]}
                ],
                "murs": {
                    "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                    "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7], [2, 2]]
                }
            },
            partie.état_partie()
        )

    #Tout les test pour les 3 cas différents de partie terminé 
    def test_partie_terminée_joueur1(self):
        partie = self.partie

        partie.joueurs = [
            {"nom": "idul", "murs": 7, "pos": [1, 9]},
            {"nom": "automate", "murs": 3, "pos": [8, 6]}
        ]
        partie.murs = {
            "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
            "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7], [2, 2]]
        }

        self.assertEqual(
            'idul',
            partie.partie_terminée()
        )

    def test_partie_terminer_joueur2(self):

        partie = self.partie

        partie.joueurs = [
            {"nom": "idul", "murs": 7, "pos": [1, 5]},
            {"nom": "automate", "murs": 3, "pos": [8, 1]}
        ]
        partie.murs = {
            "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
            "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7], [2, 2]]
        }

        self.assertEqual(
            'automate',
            partie.partie_terminée()
        )

    def test_partie_terminer_pas_terminer(self):
        partie = self.partie

        partie.joueurs = [
            {"nom": "idul", "murs": 7, "pos": [1, 5]},
            {"nom": "automate", "murs": 3, "pos": [8, 6]}
        ]
        partie.murs = {
            "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
            "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7], [2, 2]]
        }

        self.assertEqual(
            False,
            partie.partie_terminée()
        )


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
