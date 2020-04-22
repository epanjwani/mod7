from django.db import models
from django.forms import ModelForm
# Create your models here.

class League(models.Model):
    sport_type = models.CharField(max_length=50, default = "No Sport")
    user = models.CharField(max_length=50, null=True)
    league_name = models.CharField(max_length=50)
    num_teams = models.IntegerField()
    games_per_teams = models.IntegerField()
    PLAYOFF_CHOICES = (
        (16, "16"),
        (8, "8"),
        (4, "4"),
    )
    num_playoff_teams = models.IntegerField(choices=PLAYOFF_CHOICES)
    points_per_win = models.IntegerField()
    points_per_draw = models.IntegerField()
    def __str__ (self):
        return self.league_name

class Team(models.Model):
    team_name = models.CharField(max_length=50)
    league_name = models.ForeignKey(League, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    class Meta:
        ordering = ['-points']
    def __str__ (self):
        return self.team_name

class Game(models.Model):
    league_name = models.ForeignKey(League, on_delete=models.CASCADE, null=True)
    team_one = models.CharField(max_length=50)
    team_two = models.CharField(max_length=50)

