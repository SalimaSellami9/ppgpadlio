from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
import json
from django.views.decorators.http import require_POST


from .forms import RechercheReservationForm
from .models import Reservation, User, Terrain


# Page d'accueil
def home(request):
    return render(request, 'accueil.html')


# Vue de réservation via formulaire (HTML)
def reserver_formulaire(request):
    from .models import Terrain  # Assurez-vous que c'est importé en haut

def reserver_formulaire(request):
    terrains = []
    if request.method == 'POST':
        form = RechercheReservationForm(request.POST)
        if form.is_valid():
            gouvernorat = form.cleaned_data['gouvernorat']
            date = form.cleaned_data['date_jeu_souhaitee']
            nb_personnes = form.cleaned_data['nb_personnes']
            heure = form.cleaned_data['heure_debut_souhaitee']

            # Rechercher les terrains disponibles dans ce gouvernorat
            terrains = Terrain.objects.filter(gouvernorat=gouvernorat)

            return render(request, 'reservation.html', {
                'form': form,
                'terrains': terrains,
                'show_results': True,
                'date': date,
                'heure': heure,
                'nb_personnes': nb_personnes
            })
    else:
        form = RechercheReservationForm()

    return render(request, 'reservation.html', {
        'form': form,
        'show_results': False
    })

  


# API JSON pour réserver depuis le frontend JS
@csrf_exempt
def reserver_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pays = data.get("pays")
        date = data.get("date")
        nombre = data.get("nombre")
        paiement = data.get("paiement")

        # Envoyer un e-mail de confirmation
        send_mail(
            subject="Confirmation de réservation",
            message=f"Votre réservation pour {nombre} personnes le {date} à {pays} est confirmée. Paiement : {paiement}",
            from_email="ton.email@exemple.com",
            recipient_list=["utilisateur@example.com"],
        )

        return JsonResponse({"message": "Réservation réussie et email envoyé."})
    else:
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)



def rechercher_terrain(request):
    terrains = []
    form = RechercheReservationForm(request.GET or None)

    if form.is_valid():
        gouvernorat = form.cleaned_data.get('gouvernorat')
        nb_personnes = int(form.cleaned_data.get('nb_personnes'))
        terrains = Terrain.objects.filter(centre__gouvernorat=gouvernorat, etat='NR')

    return render(request, 'recherche_terrains.html', {'form': form, 'terrains': terrains})


# Connexion de l'utilisateur
def connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')

        try:
            user = User.objects.get(email=email)
            if check_password(mot_de_passe, user.mot_de_passe):
                request.session['user_id'] = user.id
                return redirect(home)
            else:
                raise User.DoesNotExist
        except User.DoesNotExist:
            return render(request, 'connecter.html', {'erreur': 'Email ou mot de passe incorrect.'})

    return render(request, 'connecter.html')


# Création de compte
def creer_compte_view(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        confirmer_mdp = request.POST.get('confirmer_mdp')
        adresse = request.POST.get('adresse')
        numero_tel = request.POST.get('numero_tel')
        niveau = request.POST.get('niveau')
        genre = request.POST.get('genre')
        role = request.POST.get('role')

        if mot_de_passe != confirmer_mdp:
            return render(request, 'creerCompte.html', {'erreur': 'Les mots de passe ne correspondent pas.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'creerCompte.html', {'erreur': 'Cet email est déjà utilisé.'})

        # Création de l'utilisateur avec mot de passe hashé
        User.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=make_password(mot_de_passe),
            adresse=adresse,
            numero_tel=numero_tel,
            niveau=niveau,
            genre=genre,
            role=role
        )

        messages.success(request, 'Compte créé avec succès. Vous pouvez vous connecter.')
        return redirect('connecter')

    return render(request, 'creerCompte.html')

@require_POST
def confirmer_reservation(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('connecter')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('connecter')

    terrain_id = request.POST.get('terrain_id')
    date = request.POST.get('date_jeu_souhaitee')
    heure = request.POST.get('heure_debut_souhaitee')
    nb_personnes = request.POST.get('nb_personnes')

    try:
        terrain = Terrain.objects.get(id=terrain_id)
    except Terrain.DoesNotExist:
        return redirect('reserver_formulaire')
    reservation = Reservation.objects.create(
        user=user,
        terrain=terrain,
        date_jeu_souhaitee=date,
        heure_debut_souhaitee=heure,
        nb_personnes=nb_personnes,
        etat_reservation='E'
    )

    return render(request, 'confirmation.html', {'reservation': reservation})