from typing import List
from extraction.team import *


class Tournament:
    def __init__(self, name, first_id, second_id):
        self.name = name
        self.first_id = first_id
        self.second_id = second_id
        self.team_ids = self._get_teams_ids_from_tournament()
        self.teams: List[Team] = self._get_teams()
        self.name_instance = {team.name: team for team in self.teams}
    
    def _get_teams_ids_from_tournament(self) -> List[int]:
        ids = []
        data = get_json_data(f"https://api.sofascore.com/api/v1/unique-tournament/{self.first_id}/season/{self.second_id}/team-events")
        tournament_team_events = data['tournamentTeamEvents']
        for team_obj in tournament_team_events.values():
            for id in team_obj.keys():
                id = int(id)
                ids.append(id)
            break
        return ids
    
    def _get_teams(self) -> List[Team]:
        teams_data = []
        for id in self.team_ids:
            new_team = Team(id)
            teams_data.append(new_team)
        return teams_data
    
    def get_round_data_from_tournament(self, round_number):
        """Return a list of Objects with each match details of a tournament round."""
        url = f"https://api.sofascore.com/api/v1/unique-tournament/{self.first_id}/season/{self.second_id}/events/round/{round_number}"
        data = get_json_data(url)
        try:
            # return list of matches
            return data["events"]
        except:
            print(f"Cannot find data from round {round_number} of {self.name}")
    
    def get_df_from_tournament_round(self, round_number: int, teams_selected: List[str]):
        """Return the data for a specific round from all teams selected in a DataFrame"""
        data = pd.DataFrame()
        carioca_round_data = self.get_round_data_from_tournament(round_number)
        teams_info = get_fetch_info(carioca_round_data, self.name_instance, teams_selected)
        for info in teams_info:
            team = self.name_instance[info["name"]]
            id = info["id"]
            field = info["field"]
            try:
                team_data = get_individual_stats_from_match(id)
                team_df = team.get_df_from_team(team_data, field)
                data = pd.concat([data, team_df])
            except Exception as ex:
                print(f"Cannot find data for {team.name} match -> {ex}")

        return data
    
    def get_tournament_inputs(self):
        """Get a Tournament inputs from user by the terminal."""
        choices = []
        for team in self.teams:
            choices.append(team.name)
        choices.sort()

        questions = [
            inquirer.Text('round', message=f"Type the round of {self.name}"),
            inquirer.Checkbox('teams', message="What teams you want to fetch data?",
                            choices=choices,
                            ),
            inquirer.Text('fname', message="Name the csv file (with .csv)"),
        ]

        answers = inquirer.prompt(questions)
        return answers
    