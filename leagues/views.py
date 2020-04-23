from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from .models import League, Team, Game

# Create your views here.
def home(request):
    username = request.session['user']
    user_leagues = League.objects.filter(user=username)
    if user_leagues:
        league_to_team_dict = {}
        for league in user_leagues:
            league_teams = Team.objects.filter(league_name=League.objects.get(league_name=league.league_name))
            if request.method == "POST":
                if league.league_name == request.POST.get("leaguename"):
                    sort_choice = request.POST.get("sort_choice")
                    string = "-" + sort_choice
                    sortedquery = league_teams.order_by(string)
                    league_to_team_dict[league.league_name] = sortedquery
                else:
                    print('newtest')
                    league_to_team_dict[league.league_name] = league_teams
            else:
                print('test')
                league_to_team_dict[league.league_name] = league_teams
        return render(request, "leagues/home.html", {'league_to_team_dict':league_to_team_dict, 'username' : request.session['user']})
    return render(request, 'leagues/home.html', {'username' : request.session['user']})

def welcomePage(request):
    return render(request, 'leagues/welcome.html')

def signUp(request):
    if request.method == 'POST':
        signupform = UserCreationForm(request.POST)
        if signupform.is_valid():
            signupform.save()
            return redirect('leagues:welcome')
    else:
        signupform = UserCreationForm()
    return render(request, 'leagues/signup.html', {'signupform': signupform})

def login(request):
    if request.method == 'POST':
        loginform = AuthenticationForm(request=request, data=request.POST)
        if loginform.is_valid():
            loginform.clean()
            username = loginform.cleaned_data.get('username')
            request.session['user'] = username
            return redirect('leagues:home')
    else:
        loginform = AuthenticationForm()
    return render(request, 'leagues/login.html', {'loginform': loginform})

def logout(request):
    del request.session['user']
    return render(request, 'leagues/logout.html')

def createLeague(request):
    if request.method == "POST":
        if request.POST.get('league_name') and request.POST.get('num_teams') and request.POST.get('games_per_teams') and request.POST.get('num_playoff_teams') and request.POST.get('points_per_win') and request.POST.get('points_per_draw') and request.POST.get("sport_type"):
            league = League()
            if League.objects.filter(league_name=request.POST.get('league_name')).exists():
                error = "League name already exists!"
                return render(request, 'leagues/createleague.html', {"error":error})
            elif int(request.POST.get('num_teams')) < 2:
                error = "Must be at least 2 teams!"
                return render(request, 'leagues/createleague.html', {"error":error})
            elif int(request.POST.get('games_per_teams')) < 1:
                error = "Must be at least 1 game per team!"
                return render(request, 'leagues/createleague.html', {"error":error})
            elif int(request.POST.get('num_playoff_teams')) < 2:
                error = "Must be at least 2 playoff teams!"
                return render(request, 'leagues/createleague.html', {"error":error})
            elif int(request.POST.get('num_playoff_teams')) > int(request.POST.get('num_teams')):
                error = "Can't have more playoff teams than actual teams!"
                return render(request, 'leagues/createleague.html', {"error":error})
            elif int(request.POST.get('points_per_win'))  < 2:
                error = "Must be at least 2 points per win!"
                return render(request, 'leagues/createleague.html', {"error":error})
            elif int(request.POST.get('points_per_draw')) < 1:
                error = "Must be at least 1 point per draw!"
                return render(request, 'leagues/createleague.html', {"error":error})
            elif int(request.POST.get('points_per_draw')) >= int(request.POST.get('points_per_win')):
                error = "A win must be more points than a draw!"
                return render(request, 'leagues/createleague.html', {"error":error})
            else:
                league.user = request.session['user']
                league.league_name = request.POST.get('league_name')
                league.num_teams = request.POST.get('num_teams')
                league.games_per_teams = request.POST.get('games_per_teams')
                league.num_playoff_teams = request.POST.get('num_playoff_teams')
                league.points_per_win = request.POST.get('points_per_win')
                league.points_per_draw = request.POST.get('points_per_draw')
                league.sports_type = request.POST.get('sport_type')
                league.save()
                request.session['league_name'] = request.POST.get('league_name')
                request.session['num_teams'] = request.POST.get('num_teams')
                return redirect('leagues:enterteams')
        else:
            error = "not all fields filled out"
            return render(request, 'leagues/createleague.html', {"error":error})
    return render(request, 'leagues/createleague.html')

def enterteams(request):
    num_teams = request.session['num_teams']
    if request.method == "POST":
        index = 1
        while (index < int(num_teams)+1):
            name = "team" + str(index)
            if request.POST.get(name) is None:
                error = "All fields must be filled out!"
                return render(request, 'leagues/enterteams.html', {"error": error})
            secondIndex = 1
            while (secondIndex < index):
                secondname = "team" + str(secondIndex)
                if (request.POST.get(secondname) == request.POST.get(name)):
                    error = "Can't have two of the same team"
                    return render(request, 'leagues/enterteams.html', {"error": error})
                secondIndex+=1
            index+=1
        new_index = 1
        while(new_index < int(num_teams)+1):
            name = "team" + str(new_index)
            team = Team()
            team.team_name = request.POST.get(name)
            team.league_name = League.objects.get(league_name=request.session['league_name'])
            team.wins = 0
            team.draws = 0
            team.losses = 0
            team.games_played = 0
            team.points = 0
            team.total_points = 0 
            team.save()
            new_index+=1
        return redirect('leagues:home')
    return render(request, 'leagues/enterteams.html')
def enterdata1(request):
    username = request.session['user']
    user_leagues = League.objects.filter(user=username)
    if request.method == "POST":
        if request.POST.get("league_choice") is not None:
            request.session['league_choice'] = request.POST.get('league_choice')
            league_name = request.POST.get('league_choice')
            league_teams = Team.objects.filter(league_name=League.objects.get(league_name=request.POST.get('league_choice')))
            return render(request,'leagues/enterdata1.html',{"league_teams":league_teams})
        elif request.POST.get("team_choice_1") and request.POST.get("team_choice_2") and request.POST.get("score_team_1") and request.POST.get("score_team_2"):
            league_teams = Team.objects.filter(league_name=League.objects.get(league_name=request.session['league_choice']))
            if int(request.POST.get("score_team_1")) >=0 and int(request.POST.get("score_team_2")) >=0:
                if (request.POST.get("team_choice_1") != request.POST.get("team_choice_2")): 
                    league_games_per_team = League.objects.get(league_name=request.session['league_choice']).games_per_teams
                    if Team.objects.get(id=request.POST.get("team_choice_1")).games_played is not league_games_per_team and Team.objects.get(id=request.POST.get("team_choice_1")).games_played is not league_games_per_team:
                        game = Game()
                        game.team_one = request.POST.get("team_choice_1")
                        game.team_two = request.POST.get("team_choice_2")
                        league = League.objects.get(league_name=request.session['league_choice'])
                        game.league_name = league
                        game.save()
                        score_team_1 = int(request.POST.get("score_team_1"))
                        score_team_2 = int(request.POST.get("score_team_2"))
                        team_one = Team.objects.get(id=request.POST.get("team_choice_1"))
                        team_two = Team.objects.get(id=request.POST.get("team_choice_2"))
                        team_one.total_points += score_team_1
                        team_two.total_points += score_team_2
                        if(score_team_1>score_team_2):
                            team_one.games_played +=1
                            team_two.games_played +=1
                            team_one.wins +=1
                            team_two.losses +=1
                            team_one.points += league.points_per_win
                        elif (score_team_1 < score_team_2):
                            team_one.games_played +=1
                            team_two.games_played +=1
                            team_two.wins +=1
                            team_one.losses +=1
                            team_two.points += league.points_per_win
                        else:
                            team_one.games_played +=1
                            team_two.games_played +=1
                            team_two.draws +=1
                            team_one.draws +=1
                            team_two.points += league.points_per_draw
                            team_one.points += league.points_per_draw
                        team_one.save()
                        team_two.save()
                        return redirect('leagues:home')
                    else:
                        error = "teams cannot exceed league max # of games!"
                        return render(request, "leagues/enterdata1.html", {"error":error, "league_teams":league_teams})
                else:
                    error = "the same team can't play themselves!"
                    return render(request, "leagues/enterdata1.html", {"error": error, "league_teams": league_teams})
            else:
                error = "scores can't be negative!"
                return render(request, "leagues/enterdata1.html", {"error": error, "league_teams": league_teams})
        else:
            league_teams = Team.objects.filter(league_name=League.objects.get(league_name=request.session['league_choice']))
            error = "not all fields are filled!"
            if request.session["league_choice"]:
                return render(request, "leagues/enterdata1.html", {"error": error, "league_teams": league_teams})
            else:
                return render(request, 'leagues/enterdata1.html', {"error": error, "user_leagues":user_leagues})      
    return render(request, 'leagues/enterdata1.html', {"user_leagues":user_leagues})          

def generatebracket(request):
    username = request.session['user']
    user_leagues = League.objects.filter(user=username)
    if request.method == "POST":
        if request.POST.get("league_choice") is not None:
            request.session['league_name_bracket'] = request.POST.get('league_choice')
            request.session['bracket_team_num'] = League.objects.get(league_name=request.POST.get('league_choice')).num_playoff_teams
            league_teams = Team.objects.filter(league_name=League.objects.get(league_name=request.POST.get('league_choice')))
            teamstopass=[]
            for team in league_teams:
                teamstopass.append(team.team_name)
            request.session['team_list'] = teamstopass
            return redirect('leagues:generatebracket2')
        else:
            error = "League not selected!"
            return render(request,'leagues/generatebracket.html',{"error":error})
    return render(request, 'leagues/enterdata1.html', {"user_leagues":user_leagues})
    
def generatebracket2(request):
    seed_to_team = {}
    if (request.session['bracket_team_num']==4):
        index = 1
        for team in request.session['team_list']:
            if (index < 5):
                seed_to_team[index]=team
                index+=1
            else:
                break
    elif (request.session['bracket_team_num']==8):
        index = 1
        for team in request.session['team_list']:
            if (index < 9):
                seed_to_team[index]=team
                index+=1
            else:
                break
    elif (request.session['bracket_team_num']==16):
        index = 1
        for team in request.session['team_list']:
            if (index < 17):
                seed_to_team[index]=team
                index+=1
            else:
                break
    return render(request, "leagues/generatebracket2.html", {"seed_to_team":seed_to_team})