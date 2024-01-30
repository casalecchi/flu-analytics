class Team:
    def __init__(self, name, primary_color, secondary_color, badge, third_color=""):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.third_color = third_color
        self.badge = badge


Botafogo = Team("BOTAFOGO", "#ffffff", "#000000", "img/bota.png")
Flamengo = Team("FLAMENGO", "#ff0000", "#000000", "img/fla.png")
Fluminense = Team("FLUMINENSE", "#A1002C", "#006A3D", "img/flu.png", third_color="#ffffff")
Vasco = Team("VASCO", "#000000", "#ffffff", "img/vasco.png", third_color="#ff0000")
