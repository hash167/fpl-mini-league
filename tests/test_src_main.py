from unittest.mock import patch, call

from src.main import GameWeek
from src.urls import API_URLS


@patch('src.main.fetch')
def test_gameweek(mock_fetch):
    gw = GameWeek()
    assert mock_fetch.call_count == 2
    calls = [call(API_URLS['static'])]
    mock_fetch.assert_has_calls(calls)
    gw.static_info = {
        'events': [
            {
                'id': 1,
                'is_current': False
            },
            {
                'id': 2,
                'is_current': True
            }
        ]
    }
    assert gw.current_game_week == 2


# @patch('src.main.fetch')
# def test_users():
#     user = User(1, 2)
