import os
import requests
from dataclasses import dataclass
from typing import List

from src.urls import API_URLS

session = requests.session()


class UrlNotFoundException(Exception):
    pass


def fetch(url, headers=None):
    response = session.get(url=url, headers=headers)
    if response.status_code > 400:
        msg = f'Unable to to fetch {url}.' \
              f'Response Code is {response.status_code}'
        raise UrlNotFoundException(msg)
    return response.json()


@dataclass(init=False)
class GameWeek:
    """
    property: Type, Description
    current_game_week: String, Current Gameweek
    elements: List, player elements returned by live gameweek
    """
    live_info: List
    static_info: List
    fixtures: List

    def _get_live_elements(self):
        return fetch(
            API_URLS["gameweek_live"].format(self.current_game_week))

    def _get_live_fixtures(self):
        return fetch(API_URLS['gameweek_fixtures']
                     .format(self.current_game_week))

    def __init__(self):
        info = fetch(API_URLS['static'])
        self.static_info = info
        self.live_info = self._get_live_elements()
        self.fixtures = self._get_live_fixtures()

    @property
    def current_game_week(self):
        events = self.static_info['events']
        for event in events:
            if event['is_current']:
                return event['id']
        return None


@dataclass(init=False)
class UserMiniLeague:
    league_id: str
    page: str
    league_users: List
    league_standings: List

    def __init__(self, league_id, page):
        self.league_id = league_id
        self.page = page
        print(page)
        ls = self._get_fpl_league_data()
        self.league_standings = ls
        self.league_users = [{
            team['id']: {
                'entry': team['entry'],
                'name': team['entry_name'],
            }} for team in ls['standings']['results']]

    def _get_fpl_league_data(self):
        """
        Use our league id to get history data from the FPL API.
        """
        url = "https://users.premierleague.com/accounts/login/"

        headers = {
            "login": os.environ.get('FPL_LOGIN'),
            "password": os.environ.get('FPL_PASSWORD'),
            "app": "plfpl-web",
            "redirect_uri": "https://fantasy.premierleague.com/a/login",
        }
        session.post(url, data=headers)
        print('login succeeded')
        self.league_standings = fetch(API_URLS['league_classic'].format(
            self.league_id,
            self.page))
        return self.league_standings


@dataclass(init=False)
class User:
    team_id: str
    picks_for_current_gameweek: List
    first_xi: List
    subs: List
    fixtures_started: List
    game_week: GameWeek

    def __init__(self, team_id, game_week):
        self.team_id = team_id

        if game_week:
            self.game_week = game_week
            user_picks = fetch(
                API_URLS['user_picks'].format(
                    self.team_id,
                    game_week.current_game_week))
            self.user_team_info = fetch(
                API_URLS['team_info'].format(self.team_id))
            self.picks = user_picks
            self.first_xi = [pick['element'] for pick in self.picks['picks']
                             if pick['position'] <= 11]
            self.subs = [pick['element'] for pick in self.picks['picks']
                         if pick['element'] not in self.first_xi]
            self.fixtures_started = [fixture['id']
                                     for fixture in self.game_week.fixtures
                                     if fixture['started']]

    def _valid_formation(players):
        positions = list(map(lambda x: x['element_type'], players))
        g = positions.count(1)
        d = positions.count(2)
        m = positions.count(3)
        f = positions.count(4)
        return all([
            g == 1,
            3 <= d <= 5,
            2 <= m <= 5,
            1 <= f <= 3,
            sum([g, d, m, f]) == 11
        ])

    @property
    def first_xi_detail(self):
        all_players = self.game_week.static_info['elements']
        first_xi_detail = {player['id']: player
                           for player in all_players
                           if player['id'] in self.first_xi}
        players = self.game_week.live_info['elements']
        for player in players:
            if player['id'] in self.first_xi:
                id = player['id']
                live_score = player['stats']['total_points']
                no_minutes = player['stats']['minutes'] == 0
                game_started = any(
                    [game['fixture'] in self.fixtures_started
                     for game in player['explain']])
                first_xi_detail[id]['live_score'] = live_score
                did_not_play = no_minutes and game_started
                first_xi_detail[id]['did_not_play'] = did_not_play

        return first_xi_detail

    @property
    def leagues(self):
        return self.user_team_info['leagues']['classic']

    @property
    def live_score(self):
        picks = self.picks
        active_chip = picks['active_chip']
        picks = picks['picks']
        subs_out = [player['id'] for player in self.first_xi_detail.values()
                    if player['did_not_play']]

        if active_chip == 'bboost':
            self.first_xi.append(self.subs)
        else:
            for sub_out in subs_out:
                i = 0
                self.first_xi.remove(sub_out)
                self.first_xi.add(self.subs[0])
                valid_formation = self._valid_formation(
                    map(lambda x: self.first_xi_detail[x], self.first_xi))
                while not valid_formation and i <= 3:
                    i += 1
                    self.first_xi.remove(self.subs[i - 1])
                    self.first_xi.add(self.subs[i])
                    valid_formation = self._valid_formation(
                        map(lambda x: self.first_xi_detail[x], self.first_xi))
                self.subs.pop(i)

        first_xi_live_scores = []
        for player in list(self.first_xi_detail.values()):
            first_xi_live_scores.append(player['live_score'])

        captain = next(pick["element"] for pick in picks if pick["is_captain"])
        print(f'Captain: {captain}, '
              f'{self.first_xi_detail[captain]["web_name"]}')
        try:
            vice_captain = next(
                pick["element"] for pick in picks
                if pick["is_vice_captain"] and pick["multiplier"] == 1)
        except StopIteration:
            vice_captain = None
        captain_points = self.first_xi_detail[captain]['live_score']
        if captain in subs_out and vice_captain:
            captain_points = self.first_xi_detail[vice_captain]['live_score']

        if active_chip == "3xc":
            captain_points *= 2

        return sum(first_xi_live_scores) + captain_points


if __name__ == "__main__":
    gw = GameWeek()
    print(gw)
