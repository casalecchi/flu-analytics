import os

class Team:
    def __init__(self, name, primary_color, secondary_color, badge, third_color=""):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.third_color = third_color
        self.badge = badge

path = os.getcwd() + '/img/'
Botafogo = Team("BOTAFOGO", "#ffffff", "#000000", path + "bota.png")
Flamengo = Team("FLAMENGO", "#ff0000", "#000000", path + "fla.png")
Fluminense = Team("FLUMINENSE", "#A1002C", "#006A3D", path + "flu.png", third_color="#ffffff")
Vasco = Team("VASCO", "#000000", "#ffffff", path +"vasco.png", third_color="#ff0000")

TEAMS = [Botafogo, Flamengo, Fluminense, Vasco]

TEAMS_OBJ = {team.name: team for team in TEAMS}
