class Team:
    def __init__(self, name, primary_color, secondary_color, id, third_color=""):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.id = id
        self.badge = f"https://api.sofascore.com/api/v1/team/{id}/image"
        self.third_color = third_color

Botafogo = Team("BOTAFOGO", "#ffffff", "#000000", 1958)
Flamengo = Team("FLAMENGO", "#ff0000", "#000000", 5981)
Fluminense = Team("FLUMINENSE", "#A1002C", "#006A3D", 1961, third_color="#ffffff")
Vasco = Team("VASCO", "#000000", "#ffffff", 1974, third_color="#ff0000")
Audax_RJ = Team("AUDAX-RJ", "#05376C", "#F48221", 85341, third_color="#ffffff")
Bangu = Team("BANGU", "#ffffff", "#E20019", 1993)
Boavista = Team("BOAVISTA", "#38A356", "#FFFFFF", 6977)
Madureira = Team("MADUREIRA", "#FFE314", "#13027C", 6980, third_color="#B30001")
Nova_Iguacu = Team("NOVA IGUAÇU", "#F28000", "#23211C", 6981, third_color="#FEFEFE")
Portuguesa_RJ = Team("PORTUGUESA-RJ", "#008F45", "#D91E25", 208067, third_color="#E6E60E")
Sampaio_Correa_RJ = Team("SAMPAIO CORREA-RJ", "#00479C", "#FFC415", 257632)
Volta_Redonda = Team("VOLTA REDONDA", "#000000", "#FEEF03", 6982, third_color="#ffffff")

TEAMS = [Botafogo, Flamengo, Fluminense, Vasco, Audax_RJ, Bangu, Boavista, Madureira, Nova_Iguacu, Portuguesa_RJ, Sampaio_Correa_RJ, Volta_Redonda]

TEAMS_OBJ = {team.name: team for team in TEAMS}
