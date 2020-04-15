from flask import Blueprint, jsonify
from flask_cors import cross_origin

from src.main import GameWeek, User, UserMiniLeague

index_blueprint = Blueprint('index', __name__)

gw = GameWeek()


@index_blueprint.route("/user/<user_id>/live_score")
@cross_origin(origin="*")
def live_score(user_id):
    user = User(team_id=user_id, game_week=gw)
    data = {
        'live_score': user.live_score
    }
    return jsonify(data)


@index_blueprint.route("/user/<user_id>/leagues")
@cross_origin(origin="*")
def user_leagues(user_id):
    user = User(team_id=user_id, game_week=gw)
    return jsonify(user.leagues)


@index_blueprint.route("/user/<user_id>/league/<league_id>")
@cross_origin(origin="*")
def league_info(user_id, league_id):
    user = User(team_id=user_id, game_week=gw)
    for league in user.leagues:
        if str(league['id']) == league_id:
            page = str(int(int(league['entry_rank']) / 50) + 1)
            user_mini_league = UserMiniLeague(league_id=league['id'], page=page)
            return jsonify(user_mini_league.league_standings)
    return jsonify({})


@index_blueprint.route("/league/<league_id>")
@cross_origin(origin="*")
def league(league_id):
    return jsonify(UserMiniLeague(league_id=league_id, page='1').league_standings)
