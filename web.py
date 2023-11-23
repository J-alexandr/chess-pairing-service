from flask import Flask, request, jsonify

from models import Player, Tournament, Team

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
            'surname': white.split('|.|')[1],
            'team_name': white.split('|.|')[2],
        },
        'black': {
            'name': black.split('|.|')[0],
            'surname': black.split('|.|')[1],
            'team_name': black.split('|.|')[2],
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
        white = find_player(tournament.teams, match['white']['name'], match['white']['surname'], match['white']['team_name'])
        black = find_player(tournament.teams, match['black']['name'], match['black']['surname'], match['black']['team_name'])
        pair = (white, black)
        tournament.rooms[0].previous_matches.append(pair)

    return tournament


@app.route('/pair', methods=['POST'])
def endpoint1():
    json_data = request.json

    num_rounds = int(json_data.get('rounds'))
    players_scores = [parse_scores(score_json) for score_json in json_data.get('scores')]
    previous_matches = [parse_match(match_json) for match_json in json_data.get('previous_matches')]
    teams = [parse_team(team_json) for team_json in json_data.get('teams')]
    tournament = create_tournament(teams, num_rounds)

    tournament.start_tournament(1)

    insert_tournament_data(tournament, players_scores, previous_matches)

    # tournament.play_rounds()

    tournament.rooms[0].sort_player_list_by_score(key=tournament.results)
    tournament.rooms[0].create_pairs()

    response = []
    for pair in tournament.rooms[0].pairs:
        white = pair[0].to_dict()
        black = pair[1].to_dict()
        response.append({
            "white": white,
            "black": black
        })
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
