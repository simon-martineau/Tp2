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
            [
                {'nom': 'Simon', 'murs': 9, 'pos': (5, 1)},
                {'nom': 'Robot', 'murs': 10, 'pos': (5, 9)},
            ],
            murs={
                'horizontaux': [(4, 4)],
                'verticaux': []
            }
        )

        self.assertEqual(
            partie.joueurs,
            [
                {'nom': 'Simon', 'murs': 9, 'pos': (5, 1)},
                {'nom': 'Robot', 'murs': 10, 'pos': (5, 9)},
            ]
        )

        self.assertEqual(
            partie.murs,
            {'horizontaux': [(4, 4)], 'verticaux': []}
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
            [{'nom': 'Simon', 'murs': 10, 'pos': (10, 1)}, 'Robot'],
            murs={
                'horizontaux': [(3, 5)],
                'verticaux': [(4, 4)]
            }
        )


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
