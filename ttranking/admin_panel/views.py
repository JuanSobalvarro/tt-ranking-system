# admin_panel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views import View

from .forms import SinglesMatchForm, DoublesMatchForm, PlayerForm

from matches.models import SinglesMatch
from matches.models import DoublesMatch

from players.models import Player

PLAYERS_PER_PAGE = 10
MATCHES_PER_PAGE = 10


class AdminLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'admin_panel/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST or None)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('/admin-panel/')
        return render(request, 'admin_panel/login.html', {'form': form})


class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/admin-panel/')

    def post(self, request):
        logout(request)
        return redirect('/admin-panel/')

def is_admin(user):
    return user.is_staff


@login_required
def dashboard(request):
    # Your dashboard view logic here
    return render(request, 'admin_panel/admin_dashboard.html')


"""
PLAYERS VIEWS
"""


@login_required
def player_list(request):
    player_list = Player.objects.all()
    paginator = Paginator(player_list, PLAYERS_PER_PAGE)  # Show PLAYERS_PER_PAGE players per page.

    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)

    return render(request, 'admin_panel/players/player_list.html', {'players': players})


@login_required
def player_add(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:player_list')
    else:
        form = PlayerForm()
    return render(request, 'admin_panel/players/player_add.html', {'form': form})


@login_required
def player_edit(request, pk):
    player = get_object_or_404(Player, id=pk)
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, 'Player updated successfully!')
            return redirect('admin_panel:player_list')  # Redirect to the player list or detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PlayerForm(instance=player)

    return render(request, 'admin_panel/players/player_edit.html', {'form': form, 'player': player})


@login_required
def player_delete(request, pk):
    player = get_object_or_404(Player, id=pk)
    if request.method == 'POST':
        player.delete()
        return redirect('admin_panel:player_list')
    return render(request, 'admin_panel/players/player_delete.html', {'player': player})


"""
MATCHES VIEWS
"""


def get_match_and_form(match_id, match_type):
    print(match_id, match_type)
    match = None
    form = None
    if match_type == 'S':
        match = get_object_or_404(SinglesMatch, id=match_id)
        form = SinglesMatchForm(instance=match)
    elif match_type == 'D':
        match = get_object_or_404(DoublesMatch, id=match_id)
        form = DoublesMatchForm(instance=match)
    return match, form


@login_required
def match_list(request):
    singles_match_list = SinglesMatch.objects.all()
    doubles_match_list = DoublesMatch.objects.all()

    singles_paginator = Paginator(singles_match_list, MATCHES_PER_PAGE)  # Show MATCHES_PER_PAGE singles matches per page.
    doubles_paginator = Paginator(doubles_match_list, MATCHES_PER_PAGE)  # Show MATCHES_PER_PAGE doubles matches per page.

    singles_page = request.GET.get('singles_page')
    doubles_page = request.GET.get('doubles_page')

    try:
        singles_matches = singles_paginator.page(singles_page)
    except PageNotAnInteger:
        singles_matches = singles_paginator.page(1)
    except EmptyPage:
        singles_matches = singles_paginator.page(singles_paginator.num_pages)

    try:
        doubles_matches = doubles_paginator.page(doubles_page)
    except PageNotAnInteger:
        doubles_matches = doubles_paginator.page(1)
    except EmptyPage:
        doubles_matches = doubles_paginator.page(doubles_paginator.num_pages)

    return render(request, 'admin_panel/matches/match_list.html', {
        'singles_matches': singles_matches,
        'doubles_matches': doubles_matches
    })

@login_required
def match_add(request):
    match_type = request.GET.get('match_type')
    form_singles = SinglesMatchForm(request.POST or None) if match_type == 'S' else None
    form_doubles = DoublesMatchForm(request.POST or None) if match_type == 'D' else None

    if request.method == 'POST':
        if match_type == 'S' and form_singles.is_valid():
            form_singles.save()
            messages.success(request, 'Singles match added successfully!')
            return redirect('admin_panel:match_list')
        elif match_type == 'D' and form_doubles.is_valid():
            form_doubles.save()
            messages.success(request, 'Doubles match added successfully!')
            return redirect('admin_panel:match_list')
        else:
            messages.error(request, 'The form has errors')

    return render(request, 'admin_panel/matches/match_add.html', {
        'match_type': match_type,
        'form_singles': form_singles,
        'form_doubles': form_doubles,
    })


@login_required
def match_update(request, pk):
    match_type = request.GET.get('match_type')
    match, form = get_match_and_form(match_id=pk, match_type=match_type)

    if request.method == 'POST':
        if match_type == 'S':
            form = SinglesMatchForm(request.POST, instance=match)
        elif match_type == 'D':
            form = DoublesMatchForm(request.POST, instance=match)

        if form.is_valid():
            form.save()
            messages.success(request, 'Match updated successfully!')
            return redirect('admin_panel:match_list')
        else:
            messages.error(request, 'There was an error with your submission.')

    return render(request, 'admin_panel/matches/match_update.html', {'form': form, 'match_type': match_type})


@login_required
def match_delete(request, pk):
    match_type = request.GET.get('match_type')
    match, _ = get_match_and_form(pk, match_type)

    if request.method == 'POST':
        match.delete()
        messages.success(request, 'Match deleted successfully!')
        return redirect('admin_panel:match_list')

    return render(request, 'admin_panel/matches/match_delete.html', {'match': match, 'match_type': match_type})
