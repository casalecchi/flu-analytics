import inquirer
import pandas as pd
from pathlib import Path
import requests
from extraction.classes import *

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

ROOT_DIR = str(Path(__file__).absolute().parent.parent.parent)


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

CARIOCA_TEAMS = [Botafogo, Flamengo, Fluminense, Vasco, Audax_RJ, Bangu, Boavista, Madureira, Nova_Iguacu, Portuguesa_RJ, Sampaio_Correa_RJ, Volta_Redonda]
CARIOCA_TEAMS_OBJ = {team.name: team for team in CARIOCA_TEAMS}

Carioca = Tournament("Carioca Série A – Taça Guanabara", 92, 56974)
Brasileirao_2023 = Tournament("Brasileirão Série A", 325, 48982)