from flask import Flask, request, jsonify

from models import Player, Tournament, Team, Room

app = Flask(__name__)


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


def parse_match(match_json):
    white = match_json.get('white')
    black = match_json.get('black')
    return {
        'white': {
            'name': white.split('|.|')[0],
            'team_name': white.split('|.|')[1],
        },
        'black': {
            'name': black.split('|.|')[0],
            'team_name': black.split('|.|')[1],
        }
    }


def create_tournament(teams: list[Team], num_rounds: int):
    tournament = Tournament('EPL', num_rounds)
    for team in teams:
        tournament.add_team(team)
    return tournament


def find_player(teams: list[Team], name, surname, team_name):
    for team in teams:
        if team.name == team_name:
            for player in team.players:
                if player.name == name and player.surname == surname:
                    return player
    return None


def insert_tournament_data(tournament: Tournament, players_scores, previous_matches):
    for score in players_scores:
        tournament.rooms[0].color_counts[score.player]['white'] = score.white
        tournament.rooms[0].color_counts[score.player]['black'] = score.black

        tournament.results[score.player]['white'] = score.white
        tournament.results[score.player]['black'] = score.black
        tournament.results[score.player]['rounds_played'] = score.rounds_played
        tournament.results[score.player]['score'] = score.score

    for match in previous_matches:
        white = find_player(tournament.teams, match['white']['name'], match['white']['name'], match['white']['team_name'])
        black = find_player(tournament.teams, match['black']['name'], match['black']['name'], match['black']['team_name'])
        pair = (white, black)
        tournament.rooms[0].previous_matches.append(pair)

    return tournament


@app.route('/pair', methods=['POST'])
def generatePairings():
    json_data = request.json
    print(f"API request: {json_data}")

    players_scores = convert_to_dict([parse_scores(score_json) for score_json in json_data.get('scores')])
    previous_matches = [parse_match(match_json) for match_json in json_data.get('previous_matches')]
    teams = [parse_team(team_json) for team_json in json_data.get('teams')]

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
    print(f"API response: {json_response.json}")
    return json_response


if __name__ == '__main__':
    print("Application build 1.0.1")
    app.run(debug=True)
