import unittest
from models import Player, Room, Tournament, sort_players_by_score
from utils import check_matching_conditions, export_results


class TestRoom(unittest.TestCase):
    def test_pair_players(self):
        player1 = Player("Player1", "Player1Surname", "Team A", 1)
        player2 = Player("Player2", "Player2Surname", "Team B", 2)
        player3 = Player("Player3", "Player3Surname", "Team A", 1)
        player4 = Player("Player4", "Player4Surname", "Team B", 2)
        player5 = Player("Player5", "Player5Surname", "Team A", 1)
        players = [player1, player2, player3, player4, player5]
        previous_pairs = [(player1, player2)]
        room = Room(1)
        room.players = players
        room.previous_matches = previous_pairs
        room.color_counts = {
            str(player1): {"white": 0, "black": 0},
            str(player2): {"white": 0, "black": 0},
            str(player3): {"white": 0, "black": 0},
            str(player4): {"white": 0, "black": 0},
            str(player5): {"white": 0, "black": 0},
        }
        room.create_pairs()
        self.assertEqual(len(room.pairs), 2)  # Two valid pairs should be formed
        self.assertNotIn((player1, player2), room.pairs)  # The previously used pair should not be included

    def test_check_matching_conditions(self):
        player1 = Player("Player1", "Player1Surname", "Team A", 1)
        player2 = Player("Player2", "Player2Surname", "Team B", 2)
        player3 = Player("Player3", "Player3Surname", "Team A", 1)
        player4 = Player("Player4", "Player4Surname", "Team B", 2)
        player5 = Player("Player5", "Player5Surname", "Team A", 1)
        player6 = Player("Player6", "Player6Surname", "Team B", 2)
        color_counts = {
            str(player1): {"white": 1, "black": 2},
            str(player2): {"white": 2, "black": 1},
            str(player3): {"white": 0, "black": 0},
            str(player4): {"white": 3, "black": 1},
            str(player5): {"white": 1, "black": 3},
            str(player6): {"white": 1, "black": 3}
        }
        previous_pairs = [(player1, player2)]
        print(player1.team == player3.team)
        # room = Room([])
        self.assertFalse(check_matching_conditions(player1, player2, color_counts, previous_pairs))  # Same position - player1 and player2 already played
        self.assertFalse(check_matching_conditions(player2, player1, color_counts, previous_pairs))  # Same position (reversed) - player1 and player2 already played
        self.assertFalse(check_matching_conditions(player1, player3, color_counts, previous_pairs))  # Same team
        self.assertFalse(check_matching_conditions(player5, player6, color_counts, previous_pairs))  # Color mismatch
        self.assertTrue(check_matching_conditions(player4, player1, color_counts, previous_pairs))   # Valid pairing


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

    def test_export_results(self):
        data = [
            {'Name_Team3_Player4 Surname_Team3_Player4 Team3_Name': {'black': 0, 'rounds_played': 1, 'score': 3, 'white': 1}},
            {'Name_Team3_Player3 Surname_Team3_Player3 Team3_Name': {'black': 1, 'rounds_played': 1, 'score': 0, 'white': 0}}
            # Add more dictionaries to the list if needed
        ]
        export_results(data=data)


if __name__ == "__main__":
    unittest.main()
