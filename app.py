import logging
import random

from flask import Flask, request, jsonify

from models import Player, Team, Room

pairing_service = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PlayerScore:
    def __init__(self, player, white, black, score, rounds_played):
        self.player = player
        self.white = white
        self.black = black
        self.score = score
        self.rounds_played = rounds_played


def parse_team(team_json):
    team_name = team_json.get('name')
    cln = team_json.get('cln')
    players = []

    for player_json in team_json.get('players'):
        player = Player(player_json.get('name'), player_json.get('surname'), team_name, cln)
        players.append(player)
    return Team(team_name, players)


def extract_all_players(teams):
    all_players = []
    for team in teams:
        all_players.extend(team.players)
    random.shuffle(all_players)
    return all_players


def convert_to_dict(player_scores: list[PlayerScore]):
    player_scores_dict = {}
    for player_score in player_scores:
        player_scores_dict[player_score.player] = player_score.__dict__
    return player_scores_dict


def parse_scores(game_json):
    player = game_json.get('player')
    white = game_json.get('white')
    black = game_json.get('black')
    score = game_json.get('score')
    rounds_played = game_json.get('rounds_played')
    return PlayerScore(player, white, black, score, rounds_played)


def find_player(teams: list[Team], name, surname, team_name):
    for team in teams:
        if team.name == team_name:
            for player in team.players:
                if player.name == name and player.surname == surname:
                    return player
    return None


@pairing_service.route('/pair', methods=['POST'])
def generate_pairings():
    json_data = request.json
    logger.info(f"API request: {json_data}")

    players_scores = convert_to_dict([parse_scores(score_json) for score_json in json_data.get('scores')])
    teams = [parse_team(team_json) for team_json in json_data.get('teams')]
    previous_matches = [
        (find_player(teams, match['white'].split('|.|')[0], match['white'].split('|.|')[0], match['white'].split('|.|')[1]),
         find_player(teams, match['black'].split('|.|')[0], match['black'].split('|.|')[0], match['black'].split('|.|')[1]))
        for match in json_data.get('previous_matches')
    ]

    room = Room(1)
    room.players = extract_all_players(teams)
    room.previous_matches = previous_matches
    room.color_counts = players_scores
    room.sort_player_list_by_score(players_scores)
    room.create_pairs()

    response = []
    for pair in room.pairs:
        response.append({
            "white": pair[0].to_dict()['name'],
            "black": pair[1].to_dict()['name']
        })

    json_response = jsonify(response)
    logger.info(f"API response: {json_response.json}")
    return json_response


if __name__ == '__main__':
    logger.info("Application build 1.1.0")
    pairing_service.run(debug=True)
