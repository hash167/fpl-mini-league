from flask import Blueprint, jsonify
from flask_cors import cross_origin

from src.main import GameWeek, User

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route("/user/<user_id>")
@cross_origin(origin="*")
def user(user_id):
    gw = GameWeek()
    user = User(team_id=user_id, game_week=gw)
    data = {
        'gw': gw.current_game_week,
        'live_score': user.live_score
    }
    return jsonify(data)
