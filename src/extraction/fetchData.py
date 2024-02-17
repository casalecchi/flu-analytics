from extraction import requests, HEADERS


def get_json_data(url):
    """Return JSON data as an Object from given URL."""
    response = requests.get(url, stream=True, headers=HEADERS)
    return response.json()

def get_individual_stats_from_match(match_id):
    """Return JSON data as an Object containing individual stats from match. Input is the match ID from sofascore."""
    json_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    return get_json_data(json_url)

def get_fetch_info(round_data: object, tournament_teams_obj, teams):
    """Return the list of teams that will be fetched. Each item of this list will contain
    the team name, id and the field (home or away)."""

    def get_team_props(name, id, field) -> object:
        return {
            "name"  : name,
            "id"    : id,
            "field" : field,
        }

    info = []
    for match in round_data:
        teams_find = 0
        for team in teams:
            if teams_find == 2: break
            field = ""
            home = match["homeTeam"]["id"]
            away = match["awayTeam"]["id"]
            if home == tournament_teams_obj[team].id:
                field = "home"
                team_obj = get_team_props(team, match["id"], field)
                info.append(team_obj)
                teams_find += 1
            elif away == tournament_teams_obj[team].id:
                field = "away"
                team_obj = get_team_props(team, match["id"], field)
                info.append(team_obj)
                teams_find += 1

    return info
