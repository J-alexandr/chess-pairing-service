import unittest
from models import Player, Room, Tournament, sort_players_by_score
from utils import check_matching_conditions


class TestRoom(unittest.TestCase):
    player1 = Player("Player1", "Player1", "Team A", 1)
    player2 = Player("Player2", "Player2", "Team B", 1)
    player3 = Player("Player3", "Player3", "Team A", 1)
    player4 = Player("Player4", "Player4", "Team B", 1)
    player5 = Player("Player5", "Player5", "Team A", 1)
    player6 = Player("Player6", "Player6", "Team B", 1)
    player7 = Player("Player7", "Player7", "Team A", 1)
    player8 = Player("Player8", "Player8", "Team B", 1)


    def test_pair_players_round1(self):
        scores = {
            str(self.player1): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
            str(self.player2): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
            str(self.player3): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
            str(self.player4): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
            str(self.player5): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
            str(self.player6): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
            str(self.player7): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
            str(self.player8): {'rounds_played': 0, 'white': 0, 'black': 0, 'score': 0},
        }
        room = Room(1)
        room.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6, self.player7, self.player8]
        room.previous_matches = []
        room.color_counts = scores
        room.sort_player_list_by_score(scores)
        room.create_pairs()
        self.assertEqual(4, len(room.pairs))

    def test_pair_players_round2(self):
        scores = {
            str(self.player1): {'rounds_played': 1, 'white': 1, 'black': 0, 'score': 3},
            str(self.player2): {'rounds_played': 1, 'white': 0, 'black': 1, 'score': 1},
            str(self.player3): {'rounds_played': 1, 'white': 1, 'black': 0, 'score': 1},
            str(self.player4): {'rounds_played': 1, 'white': 0, 'black': 1, 'score': 3},
            str(self.player5): {'rounds_played': 1, 'white': 1, 'black': 0, 'score': 2},
            str(self.player6): {'rounds_played': 1, 'white': 0, 'black': 1, 'score': 2},
            str(self.player7): {'rounds_played': 1, 'white': 1, 'black': 0, 'score': 1},
            str(self.player8): {'rounds_played': 1, 'white': 0, 'black': 1, 'score': 3},
        }
        room = Room(1)
        room.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6, self.player7, self.player8]
        room.previous_matches = [(self.player1, self.player2), (self.player3, self.player4), (self.player5, self.player6), (self.player7, self.player8)]
        room.color_counts = scores
        room.sort_player_list_by_score(scores)
        room.create_pairs()
        self.assertEqual([(self.player1, self.player4), (self.player8, self.player5), (self.player6, self.player3), (self.player2, self.player7)], room.pairs)

    def test_pair_players_round3(self):
        scores = {
            str(self.player1): {'rounds_played': 2, "white": 2, "black": 0, 'score': 6},
            str(self.player2): {'rounds_played': 2, "white": 1, "black": 1, 'score': 3},
            str(self.player3): {'rounds_played': 2, "white": 1, "black": 1, 'score': 4},
            str(self.player4): {'rounds_played': 2, "white": 0, "black": 2, 'score': 4},
            str(self.player5): {'rounds_played': 2, "white": 1, "black": 1, 'score': 5},
            str(self.player6): {'rounds_played': 2, "white": 1, "black": 1, 'score': 3},
            str(self.player7): {'rounds_played': 2, 'white': 2, 'black': 0, 'score': 3},
            str(self.player8): {'rounds_played': 2, 'white': 1, 'black': 1, 'score': 4},
        }
        room = Room(1)
        room.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6, self.player7, self.player8]
        room.previous_matches = [(self.player1, self.player2), (self.player3, self.player4), (self.player5, self.player6), (self.player7, self.player8), (self.player1, self.player4), (self.player8, self.player5), (self.player6, self.player3), (self.player2, self.player7)]
        room.color_counts = scores
        room.sort_player_list_by_score(scores)
        room.create_pairs()
        self.assertEqual([(self.player8, self.player1), (self.player4, self.player5), (self.player3, self.player2), (self.player6, self.player7)], room.pairs)

    def test_pair_players_round4(self):
        scores = {
            str(self.player1): {'rounds_played': 3, "white": 2, "black": 1, 'score': 9},
            str(self.player2): {'rounds_played': 3, "white": 1, "black": 2, 'score': 6},
            str(self.player3): {'rounds_played': 3, "white": 2, "black": 1, 'score': 5},
            str(self.player4): {'rounds_played': 3, "white": 1, "black": 2, 'score': 7},
            str(self.player5): {'rounds_played': 3, "white": 1, "black": 2, 'score': 6},
            str(self.player6): {'rounds_played': 3, "white": 2, "black": 1, 'score': 5},
            str(self.player7): {'rounds_played': 3, 'white': 2, 'black': 1, 'score': 5},
            str(self.player8): {'rounds_played': 3, 'white': 2, 'black': 1, 'score': 1},
        }
        room = Room(1)
        room.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6, self.player7, self.player8]
        room.previous_matches = [(self.player1, self.player2), (self.player3, self.player4), (self.player5, self.player6), (self.player7, self.player8), (self.player1, self.player4), (self.player8, self.player5), (self.player6, self.player3), (self.player2, self.player7), (self.player8, self.player1), (self.player4, self.player5), (self.player3, self.player2), (self.player6, self.player7)]
        room.color_counts = scores
        room.sort_player_list_by_score(scores)
        room.create_pairs()
        self.assertEqual([(self.player1, self.player6), (self.player7, self.player4), (self.player5, self.player2), (self.player3, self.player8)], room.pairs)

    def test_pair_players(self):
        players = [self.player1, self.player2, self.player3, self.player4, self.player5]
        previous_pairs = [(self.player1, self.player2)]
        room = Room(1)
        room.players = players
        room.previous_matches = previous_pairs
        room.color_counts = {
            str(self.player1): {"white": 0, "black": 0},
            str(self.player2): {"white": 0, "black": 0},
            str(self.player3): {"white": 0, "black": 0},
            str(self.player4): {"white": 0, "black": 0},
            str(self.player5): {"white": 0, "black": 0},
        }
        room.create_pairs()
        self.assertEqual(len(room.pairs), 2)  # Two valid pairs should be formed
        self.assertNotIn((self.player1, self.player2), room.pairs)  # The previously used pair should not be included

    def test_check_matching_conditions(self):
        color_counts = {
            str(self.player1): {"white": 1, "black": 2},
            str(self.player2): {"white": 2, "black": 1},
            str(self.player3): {"white": 0, "black": 0},
            str(self.player4): {"white": 3, "black": 1},
            str(self.player5): {"white": 1, "black": 3},
            str(self.player6): {"white": 1, "black": 3}
        }
        previous_pairs = [(self.player1, self.player2)]

        self.assertFalse(check_matching_conditions(self.player1, self.player2, color_counts, previous_pairs))  # Same position - player1 and player2 already played
        self.assertFalse(check_matching_conditions(self.player2, self.player1, color_counts, previous_pairs))  # Same position (reversed) - player1 and player2 already played
        self.assertFalse(check_matching_conditions(self.player1, self.player3, color_counts, previous_pairs))  # Same team
        self.assertFalse(check_matching_conditions(self.player5, self.player6, color_counts, previous_pairs))  # Color mismatch
        self.assertTrue(check_matching_conditions(self.player4, self.player1, color_counts, previous_pairs))   # Valid pairing


    def test_sort_players_by_score(self):
        room = Room("Room 1")

        players = [
            Player("E3", "SE3", "Team5_Name", 8),
            Player("E9", "SE9", "Team5_Name", 8),
            Player("E4", "SE4", "Team5_Name", 8),
            Player("E10", "SE10", "Team5_Name", 8),
        ]
        for player in players:
            room.add_players(player)

        # Assign scores to players
        scores = [6, 4, 8, 5]  # Example scores, you can modify them as needed
        tournament_results = {}
        for i, player in enumerate(room.players):
            tournament_results[str(player)] = {
                'black': 0,
                'rounds_played': 2,
                'score': scores[i],
                'white': 2
            }
        tournament = Tournament('EPL', 3)
        tournament.results = tournament_results
        print(tournament.results)

        # Sort players by score
        sorted_players = sort_players_by_score(room.players, tournament.results)

        # Verify the sorting results
        expected_order = [players[2], players[0], players[3], players[1]]  # Corrected expected order based on the assigned scores

        assert sorted_players == expected_order
        print("Test passed!")


if __name__ == "__main__":
    unittest.main()
