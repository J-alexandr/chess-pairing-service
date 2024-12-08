import csv
from typing import Dict, List, Tuple


def check_matching_conditions(p1, p2, color_counts: Dict, previous_pairs: List[Tuple]):
    if p1.team == p2.team:
        return False
    elif (p1, p2) in previous_pairs or (p2, p1) in previous_pairs:
        return False
    elif (color_counts[str(p1)]['white'] - color_counts[str(p1)]['black']) >= 2 and (color_counts[str(p2)]['white'] - color_counts[str(p2)]['black']) >= 2:
        return False
    elif (color_counts[str(p1)]['black'] - color_counts[str(p1)]['white']) >= 2 and (color_counts[str(p2)]['black'] - color_counts[str(p2)]['white']) >= 2:
        return False
    else:
        return True


def export_results(data: Dict):
    print(data)
    # Extract the keys from the first dictionary to determine the fieldnames for the CSV file
    fieldnames = ['Name', 'rounds_played', 'white', 'black', 'score']

    # Specify the name of the output CSV file
    filename = 'final_result.csv'

    # Open the CSV file in write mode
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row with fieldnames
        writer.writerow(fieldnames)

        # Write each row of data to the CSV file
        for player_name, player_result in data.items():
            player_result_values = list(player_result.values())
            row = [player_name] + player_result_values
            writer.writerow(row)

    print(f"CSV file '{filename}' has been successfully created.")


def export_ongoing_tournament(teams: List, tournament_name):
    filename = 'ongoing_' + tournament_name + '_initial.csv'
    fieldnames = ['Player', 'Team']
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row with fieldnames
        writer.writerow(fieldnames)

        # Write each row of data to csv file
        for team in teams:
            for player in team.players:
                writer.writerow([player, team.name])


def export_round_tournament(pairs: List, round_number: int, tournament_name: str, room_number):
    filename = f'round{round_number}_{tournament_name}.csv'
    fieldnames = ['White', 'Black', 'Room_Number']
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row with fieldnames
        writer.writerow(fieldnames)

        # Write each row of data to csv file
        for pair in pairs:
            writer.writerow([pair[0], pair[1], room_number])


def pick_positions(w1, b1, w2, b2):
    if w1 - b1 < 2 and b2 - w2 < 2:
        return 1
    else:
        return 2


def prompt_for_num_rooms(recommended):
    while True:
        num_rooms = input('Input desired number of rooms or press enter to continue:  ')
        if num_rooms == '':
            return recommended
        elif num_rooms.isnumeric():
            print('It was numeric')
            return int(num_rooms)
        else:
            print('Invalid Input')


def simulate_match(pair: Tuple):
    if len(pair) != 2:
        print('wrong format')
    winner_options = {
        'Black Wins': 'B',
        'White Wins': 'W',
        'Draw': 'D',
        'Not Showing': 'N'
    }
    tries = 0
    print(f'{str(pair[0])} VS {str(pair[1])}')
    while True:
        winner = input(f'Select Outcome \n {winner_options}: \n ')
        if winner.upper() == 'B':
            return {str(pair[0]): 1, str(pair[1]): 3}
        elif winner.upper() == 'W':
            return {str(pair[0]): 3, str(pair[1]): 1}
        elif winner.upper() == 'D':
            return {str(pair[0]): 2, str(pair[1]): 2}
        elif winner.upper() == 'N':
            return {str(pair[0]): 0, str(pair[1]): 0}
        elif tries >= 4:
            return {str(pair[0]): 0, str(pair[1]): 0}
        else:
            tries += 1
            print('invalid input')


def suggest_number_of_rooms(size):
    if size < 100:
        return 1
    else:
        return max(1, size // 50)

