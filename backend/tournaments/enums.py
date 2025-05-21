from django.db import models

class SexType(models.TextChoices):
    Masculine = "M", "Masculine"
    Feminine = "F", "Feminine"
    Mixed = "X", "Mixed"


class TournamentStage(models.TextChoices):
    FINAL = "F", "Final"
    SEMIFINAL = "SF", "Semifinal"
    QUARTERFINAL = "QF", "Quarterfinal"
    KNOCKOUT = "KO", "Knockout"
    GROUP_STAGE = "GS", "Group Stage"
    ROUND_OF_16 = "R16", "Round of 16"
    ROUND_OF_32 = "R32", "Round of 32"
    ROUND_OF_64 = "R64", "Round of 64"
    ROUND_OF_128 = "R128", "Round of 128"


class TournamentStatus(models.TextChoices):
    IN_PROGRESS = "IP", "In Progress"
    COMPLETED = "C", "Completed"
    CANCELLED = "CC", "Cancelled"
    SCHEDULED = "S", "Scheduled"
    POSTPONED = "P", "Postponed"


class TournamentType(models.TextChoices):
    Singles = "S", "Singles"
    Doubles = "D", "Doubles"
    Teams = "T", "Teams"
