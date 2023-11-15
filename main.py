#pairing alghorithm run python main.py then
#input the teams name path/teamname.csv recursively
#input number of round
#input number of rooms just 1
#round is exported and results are asked for each game when last result has been input it will create following round
import random
import timeit
from typing import List, Dict, Tuple

import pandas as pd

from models import Player, Tournament, Room, Team
from utils import export_ongoing_tournament, export_results


def get_tournament_info() -> List:
    tname = input('Input turnament name: ')
    number_of_teams = input('Input Number of teams: ')
    number_of_rounds = input('Input number of rounds: ')
    tdate = input('Input Date with no spaces: ')

    return [tname + tdate, int(number_of_rounds), int(number_of_teams)]


def load_team_data():
    output = []
    while True:
        file_path = input('Please input filepath e.g teams/<filename.csv>')
        print('Enter "FINISH" to end')
        if file_path.upper() == "FINISH":
            break
        try:
            df = pd.read_csv(file_path, sep=',')
            output.append(df)
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
    return output


def create_team(data: pd.DataFrame):
    team_name = data.columns[0]
    cln = data.columns[1]
    players = []

    for index, row in data.iterrows():
        player = Player(row[0], row[1], team_name, cln)
        players.append(player)
    return Team(team_name, players)


def generate_pairings(teams, pairingz):
    # Generate pairings for each round
    pairings = []
    for team in teams:
        players = team.players.copy()
        random.shuffle(players)
        pairings.extend(players[i:i + 2] for i in range(0, len(players), 2))
    pairingz.append(pairings)


def create_tournament():
    pass


def generate_pairings_v1(teams: List, pairings):
    pairs = []
    teams_copy = teams.copy()
    # random.shuffle(teams_copy)
    pool = [player for team in teams_copy for player in team.players]
    random.shuffle(pool)
    print(pool)
    print(f'lenght of pool {len(pool)}')

    while len(pool) >= 2:
        pool_size = len(pool)
        player1 = pool.pop()
        stack = set()
        indices = [i for i in range(pool_size - 1)]
        while True:
            indices = [i for i in indices if i not in stack]
            print(f'indicies: {indices}')
            print(f'pool size {pool_size}')
            sample_index = random.choice(indices)
            print(f'sample: index: {sample_index}')

            # player2 = random.sample(pool, 1)[0]
            if sample_index in stack:
                continue

            print(f'Just befor subscripting: {len(pool)}')
            player2 = pool[sample_index]
            stack.add(sample_index)

            if player1.team != player2.team:
                pool.remove(player2)
                pairs.append((player1.name, player2.name))
                break
            elif all(player.team == pool[0].team for player in pool[1:]):
                # The team attribute of all items in the list is the same
                print('No more players to pair')
                break
            else:
                continue
    return pairs


def main():
    teams = [create_team(item) for item in load_team_data()]

    tn = input('Input Desired Number of rounds')
    tn = int(tn)
    tournament = Tournament('EPL', tn)
    for team in teams:
        tournament.add_team(team)

    export_ongoing_tournament(tournament.teams, tournament.name)
    print(tournament.teams)
    tournament.start_tournament()
    tournament.play_rounds()
    export_results(tournament.results)


# TODO: Add functions to generate and store state and metadata data for Tournament
# TODO: Write function to save generated data after each round
# TODO: Prompt user to either continue or stop and save progress after each round
# TODO: Finish code for simulating match for each round

if __name__ == '__main__':
    main()
