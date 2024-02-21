from extraction import requests, HEADERS


def get_json_data(url):
    """Return JSON data as an Object from given URL."""
    response = requests.get(url, stream=True, headers=HEADERS)
    return response.json()

def get_players_stats_by_match(match_id):
    """Return JSON data as an Object containing individual stats from match. Input is the match ID from sofascore."""
    json_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    return get_json_data(json_url)

def get_match_data(match_id):
    url = f"https://api.sofascore.com/api/v1/event/{match_id}"
    return get_json_data(url)['event']

def get_round_matches(unique_id, season_id, round_number):
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{unique_id}/season/{season_id}/events/round/{round_number}"
    return get_json_data(url)['events']

def get_teams_stats_by_match(match_id):
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
    return get_json_data(url)['statistics']

def get_last_matches_data(team_id, page):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/{page}"
    return get_json_data(url)['events'] # last 30 matches from team

def get_player_data(player_id, unique_id, season_id):
    url = f"https://api.sofascore.com/api/v1/player/{player_id}/unique-tournament/{unique_id}/season/{season_id}/statistics/overall"
    return get_json_data(url)

def get_team_data(team_id, unique_id, season_id):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/unique-tournament/{unique_id}/season/{season_id}/statistics/overall"
    return get_json_data(url)['statistics']
