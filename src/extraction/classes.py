class SofaStats:
    Individual_Stats = [
        "totalPass",
        "accuratePass",
        "totalLongBalls",
        "accurateLongBalls",
        "goalAssist",
        "totalCross",
        "accurateCross",
        "aerialLost",
        "aerialWon",
        "duelLost",
        "duelWon",
        "challengeLost",
        "dispossessed",
        "totalContest",
        "wonContest",
        "shotOffTarget",
        "onTargetScoringAttempt",
        "goals",
        "totalClearance",
        "outfielderBlock",
        "interceptionWon",
        "totalTackle",
        "errorLeadToAShot",
        "ownGoals",
        "wasFouled",
        "fouls",
        "totalOffside",
        "goodHighClaim",
        "saves",
        "totalKeeperSweeper",
        "accurateKeeperSweeper",
        "totalOffside",
        "minutesPlayed",
        "touches",
        "rating",
        "possessionLostCtrl",
        "expectedGoals",
        "keyPass",
        "expectedAssists",
    ]

    Num_Individual_Stats = len(Individual_Stats)


class Team:
    def __init__(self, name, primary_color, secondary_color, id, third_color=""):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.id = id
        self.badge = f"https://api.sofascore.com/api/v1/team/{id}/image"
        self.third_color = third_color


class Tournament:
    def __init__(self, name, first_id, second_id):
        self.name = name
        self.first_id = first_id
        self.second_id = second_id