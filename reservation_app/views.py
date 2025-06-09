from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .forms import  RechercheReservationForm
from .models import Reservation, User, Terrain


def home(request):
    return render(request, 'home.html')



def reserver(request):
    if request.method == 'POST':
        form = RechercheReservationForm(request.POST)
        if form.is_valid():
            user = User.objects.first()  

            reservation = Reservation.objects.create(
                user=user,
                terrain=form.cleaned_data['terrain'],
                date_jeu_souhaitee=form.cleaned_data['date_jeu_souhaitee'],
                heure_debut_souhaitee="10:00",
                nb_personnes=form.cleaned_data['nb_personnes'],
                etat_reservation='E'
            )
            return render(request, 'confirmation.html', {'reservation': reservation})
    else:
        form = RechercheReservationForm()

    return render(request, 'reservation.html', {'form': form})



def rechercher_terrain(request):
    terrains = []
    gouvernorat = request.GET.get('gouvernorat')
    nb_personnes = request.GET.get('nb_personnes')

    if gouvernorat and nb_personnes:
        try:
            nb_personnes = int(nb_personnes)
            if nb_personnes == 4:
                terrains = Terrain.objects.filter(gouvernorat=gouvernorat)
        except ValueError:
            pass

    return render(request, 'recherche_terrains.html', {'terrains': terrains})
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages 

@csrf_exempt
def reserver(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pays = data.get("pays")
        date = data.get("date")
        nombre = data.get("nombre")
        paiement = data.get("paiement")
        send_mail(
            subject="Confirmation de réservation",
            message=f"Votre réservation pour {nombre} personnes le {date} à {pays} est confirmée. Paiement : {paiement}",
            from_email="ton.email@exemple.com", 
            recipient_list=["utilisateur@example.com"], 
        )

        return JsonResponse({"message": "Réservation réussie et email envoyé."})
    else:
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)
def home(request):
    return render(request, 'accueil.html')

def connexion_view(request):
    return render(request, 'connecter.html')
#connecter 

def connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'connecter.html', {'erreur': 'Email ou mot de passe incorrect.'})

        if user.mot_de_passe == mot_de_passe:
            # Connexion réussie — ici, tu peux par exemple stocker l'ID utilisateur en session
            request.session['user_id'] = user.id
            return redirect(home)  # rediriger vers une page après connexion
        else:
            return render(request, 'connecter.html', {'erreur': 'Email ou mot de passe incorrect.'})

    return render(request, 'connecter.html')



#def creer_compte_view(request):
 #   return render(request, 'creerCompte.html')

#creation de compte 
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
            return render(request, 'creerCompte.html', {
                'erreur': 'Les mots de passe ne correspondent pas.'
            })

        # Vérifie si l'utilisateur existe déjà
        if User.objects.filter(email=email).exists():
            return render(request, 'creerCompte.html', {
                'erreur': 'Cet email est déjà utilisé.'
            })

        # Crée le nouvel utilisateur
        User.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=mot_de_passe,  # à sécuriser avec hash pour une vraie app
            adresse=adresse,
            numero_tel=numero_tel,
            niveau=niveau,
            genre=genre,
            role=role
        )

        messages.success(request, 'Compte créé avec succès. Vous pouvez vous connecter.')
        return redirect('connecter')    
    return render(request, 'creerCompte.html')