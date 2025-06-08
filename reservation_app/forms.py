from django import forms
from .models import Terrain

class ReservationForm(forms.Form):
    gouvernorat = forms.ChoiceField(choices=[
        ('Tunis', 'Tunis'), ('Ariana', 'Ariana'), ('Ben Arous', 'Ben Arous'),
        ('Manouba', 'Manouba'), ('Sfax', 'Sfax'), ('Sousse', 'Sousse'),
        ('Gabès', 'Gabès'), ('Nabeul', 'Nabeul'), ('Monastir', 'Monastir'),
        ('Bizerte', 'Bizerte')
    ])
    date_jeu_souhaitee = forms.DateField(widget=forms.SelectDateWidget)
    nb_personnes = forms.ChoiceField(choices=[(i, f"{i} personne(s)") for i in range(1, 5)])
    mode_paiement = forms.ChoiceField(choices=[
        ('tous', 'Tous le terrain'),
        ('1part', 'Une part'),
        ('2part', 'Deux parts'),
        ('3part', 'Trois parts'),
        ('sur_place', 'Sur place'),
    ])
from .models import Reservation

class RechercheReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_jeu_souhaitee', 'heure_debut_souhaitee', 'nb_personnes']
class RechercheTerrainForm(forms.Form):
    gouvernorat = forms.ChoiceField(choices=[
        ('Tunis', 'Tunis'), ('Ariana', 'Ariana'), ('Ben Arous', 'Ben Arous'),
        ('Manouba', 'Manouba'), ('Sfax', 'Sfax'), ('Sousse', 'Sousse'),
        ('Gabès', 'Gabès'), ('Nabeul', 'Nabeul'), ('Monastir', 'Monastir'),
        ('Bizerte', 'Bizerte')
    ])
