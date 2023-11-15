import unittest
from models import Player, Room
from main import check_matching_conditions


class TestRoom(unittest.TestCase):
    # def test_pair_players(self):
    #     player1 = Player("Player1", "Player1Surname", "Team A", 1)
    #     player2 = Player("Player2", "Player2Surname", "Team B", 2)
    #     player3 = Player("Player3", "Player3Surname", "Team A", 1)
    #     player4 = Player("Player4", "Player4Surname", "Team B", 2)
    #     player5 = Player("Player5", "Player5Surname", "Team A", 1)
    #     players = [player1, player2, player3, player4, player5]
    #     previous_pairs = [(player1, player2)]
    #     room = Room(players)
    #     pairs = room.pair_players(previous_pairs)
    #     self.assertEqual(len(pairs), 2)  # Two valid pairs should be formed
    #     self.assertNotIn((player1, player2), pairs)  # The previously used pair should not be included

    def test_check_matching_conditions(self):
        player1 = Player("Player1", "Player1Surname", "Team A", 1)
        player2 = Player("Player2", "Player2Surname", "Team B", 2)
        player3 = Player("Player3", "Player3Surname", "Team A", 1)
        player4 = Player("Player4", "Player4Surname", "Team B", 2)
        player5 = Player("Player5", "Player5Surname", "Team A", 1)
        player6 = Player("Player6", "Player6Surname", "Team B", 2)
        cc = {
            player1: {"white": 1, "black": 2},
            player2: {"white": 2, "black": 1},
            player3: {"white": 0, "black": 0},
            player4: {"white": 3, "black": 1},
            player5: {"white": 1, "black": 3},
            player6: {"white": 1, "black": 3}
        }
        previous_pairs = [(player1, player2)]
        print(player1.team == player3.team)
        # room = Room([])
        self.assertFalse(check_matching_conditions(player1, player2, cc, previous_pairs))  # Same position
        self.assertFalse(check_matching_conditions(player2, player1, cc, previous_pairs))  # Same position (reversed)
        self.assertFalse(check_matching_conditions(player1, player3, cc, previous_pairs))  # same team
        self.assertFalse(check_matching_conditions(player5, player6, cc, previous_pairs))  # color mismatch
        self.assertTrue(check_matching_conditions(player4, player1, cc, previous_pairs))  # Valid pairing


if __name__ == "__main__":
    unittest.main()
