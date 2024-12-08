import csv
import time
from abc import ABC, abstractmethod
import random
from typing import List, AnyStr, Dict
from itertools import zip_longest

from utils import pick_positions, check_matching_conditions, simulate_match, export_round_tournament


class Player:
    def __init__(self, name, surname, team, class_list_number):
        self.serial_number = None
        self.name = name
        self.surname = surname
        self.team = team
        self.class_list_number = class_list_number

    def set_serial_number(self, sn):
        self.serial_number = sn

    def __repr__(self):
        return f"Player(name='{self.name}', surname='{self.surname}', team='{self.team}', class_list_number={self.class_list_number})"

    def __str__(self):
        return f"{self.name} {self.surname} {self.team}"

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'class_list_number': self.class_list_number,
            'team': self.team
        }


class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.players = []
        self.pairs = []
        self.previous_matches = []
        self.color_counts = {}  # Dictionary to store the color counts

    def add_pairs(self, pair):
        self.pairs.append(pair)

    def add_players(self, player: Player):
        self.players.append(player)

    def create_pairs(self):
        all_players = self.players.copy()
        while len(all_players) >= 2:
            i = 0
            first_pick = all_players.pop(i)
            pool_size = len(all_players)
            for sample_index in range(pool_size):
                if check_matching_conditions(first_pick, all_players[sample_index], self.color_counts, self.previous_matches):
                    second_pick = all_players.pop(sample_index)
                    positions = pick_positions(
                        self.color_counts[str(first_pick)]['white'],
                        self.color_counts[str(first_pick)]['black'],
                        self.color_counts[str(second_pick)]['white'],
                        self.color_counts[str(second_pick)]['black']
                    )
                    if positions == 1:
                        self.add_pairs((first_pick, second_pick))
                        self.color_counts[str(first_pick)]['white'] += 1
                        self.color_counts[str(second_pick)]['black'] += 1
                    else:
                        self.add_pairs((second_pick, first_pick))
                        self.color_counts[str(second_pick)]['white'] += 1
                        self.color_counts[str(first_pick)]['black'] += 1
                    break

                elif sample_index == pool_size - 1:
                    # print(f'COULD NOT MATCH {str(first_pick)} WITH ANY PLAYER')
                    continue
                else:
                    continue

    def simulate_match(self, round_number: int, tournament_name: str, room_number: int, key: List) -> List[Dict]:
        outcomes = []
        self.sort_player_list_by_score(key=key)
        self.create_pairs()  # generate pairs
        export_round_tournament(self.pairs, round_number, tournament_name, room_number)
        for pair in self.pairs:
            outcome = simulate_match(pair)
            outcomes.append(outcome)
            self.previous_matches.append(pair)
        return outcomes

    def sort_player_list_by_score(self, key):
        self.players = sort_players_by_score(self.players, key)
        print(self.players)

    def post_init(self):
        for player in self.players:
            self.color_counts[str(player)] = {"white": 0, "black": 0}

    def reset_pairs(self):
        self.pairs = []

    def __repr__(self):
        return f"Room(pairs='{self.pairs}', players='{self.players}')"


class Team:
    def __init__(self, name: AnyStr, players: List[Player]):
        self.name = name
        self.players = players

    def __iter__(self):
        return iter(self.players)

    def __repr__(self):
        return f"Team(name='{self.name}', players='{len(self.players)}'"


class Tournament:
    def __init__(self, name, num_rounds):
        self.name = name
        # self.num_teams = len(self.teams)
        self.num_rounds = num_rounds
        self.status = 'Initialized'
        self.teams = []
        # self.pairings = []
        self.results = {}
        self.rooms = []

    def add_team(self, team):
        self.teams.append(team)

    def create_player_pool_for_rooms(self) -> List[Player]:
        player_pool = []
        teams_copy = self.teams.copy()
        # Shuffle the arrangement of players in each team
        for team_copy in teams_copy:
            random.shuffle(team_copy.players)
        # Add players sequentially from each team until every team has been exhausted
        for items in zip_longest(*self.teams):
            for item in items:
                if item is not None:
                    print(str(item))
                    player_pool.append(item)
        return player_pool

    def generate_pairings(self):
        # Generate pairings logic goes here
        pass

    def input_results(self, round_num, results):
        # Update round results based on user input
        # self.results.append(results)
        pass

    def export_pairings(self):
        # Export pairings to a file
        pass

    def export_round_results(self, round_num):
        # Export round results to a file
        pass

    def export_team_scores(self):
        # Calculate and export team scores to a file
        pass

    def populate_room(self, player_pool) -> None:
        # Initialize index variable
        player_index = 0
        # Iterate until all players are assigned
        while player_index < len(player_pool):
            for room in self.rooms:
                if player_index >= len(player_pool):  # Check if all players are assigned
                    break

                player = player_pool[player_index]  # Select the player at current index
                room.add_players(player)  # Add the player to the current room
                player_index += 1  # Move to the next player

    def start_tournament(self, num_rooms) -> None:
        player_pool = self.create_player_pool_for_rooms()  # generate a randomized pool of players
        # num_rooms = suggest_number_of_rooms(len(player_pool))
        # print(f"Suggeted Number Of Rooms is: {num_rooms}")
        # num_rooms = prompt_for_num_rooms(num_rooms)  # get number of rooms as input from user

        # Create room(s)
        for i in range(num_rooms):
            self.rooms.append(Room(i))
            # pprint.pprint(self.rooms)

        # Initialize output result template
        for player in player_pool:
            self.results.update(
                {str(player): {
                    'rounds_played': 0,
                    'white': 0,
                    'black': 0,
                    'score': 0
                }}
            )

        # Populate each room
        self.populate_room(player_pool)
        # Initialize each room
        for room in self.rooms:
            room.post_init()

    def play_rounds(self) -> None:
        for i in range(1, self.num_rounds + 1):
            round_pairs = []
            for room_num, room in enumerate(self.rooms):
                print(f'\nROUND:{i}, ROOM:{room_num + 1} \n')
                # room.sort_player_list_by_score(self.results)
                # export_round_tournament(room.pairs, i, self.name, room_num + 1)  # Export pairing to csv file
                outcomes = room.simulate_match(i, tournament_name=self.name, room_number=room_num + 1, key=self.results)
                room.reset_pairs()

                # Update the results dict
                for game_outcome in outcomes:
                    for player, score in game_outcome.items():
                        self.results[player]['rounds_played'] += 1
                        self.results[player]['score'] += score
                        self.results[player]['white'] = room.color_counts[player]['white']
                        self.results[player]['black'] = room.color_counts[player]['black']

        # pprint.pprint(self.results)

    def save_tournament_metadata(self, filename):
        # Extract the keys from the first dictionary to determine the fieldnames for the CSV file
        fieldnames = ['Tournament_name', 'date', 'rounds', 'status']
        # Open the CSV file in write mode
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row with fieldnames
            writer.writerow(fieldnames)

            # Write the rows
            writer.writerows([
                self.name,
                time.time(),
                self.num_rounds,
                self.status
            ])

    def __repr__(self):
        return f"Tournament(name='{self.name}', num_teams={len(self.teams)}, num_rounds={self.num_rounds})"


class PairingAlgorithm(ABC):
    @abstractmethod
    def generate_pairings(self, tournament):
        pass


def sort_players_by_score(player_list: List, results: Dict):
    sorted_players = sorted(player_list, key=lambda player: results[str(player)]['score'], reverse=True)
    return sorted_players
