from django import forms
from .models import *
from django.db.models import F



class CategorieForm(forms.ModelForm):

	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	designation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = Categorie
		fields = '__all__'


class GroupeForm(forms.ModelForm):
	designation 		= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	nb_mouton_acheter 	= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	prix_achat 			= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	date_achat 			= forms.DateField(widget=forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control ','placeholder':'JJ/MM/AAAA'}),input_formats=('%d/%m/%Y','%d-%m-%Y','%Y/%m/%d','%Y-%m-%d' ), required = True )
	lieux_achat 		= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = Groupe
		fields = (
			'designation',
			'nb_mouton_acheter',
			'prix_achat',
			'date_achat',
			'lieux_achat',
			)

class ClientForm(forms.ModelForm):
	nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)

	class Meta:
		model = Client
		fields = (
			'nom',
			'prenom',
			'adresse',
			'tel',
			'email',
			)



class MoutonForm(forms.ModelForm):
	choices = (
		('#000000','Noir'),
		('#277ec1','Bleu'),
		('#bc0000','Rouge'),
		('#a6e228','Vert'),
	)
	# num = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	categorie = forms.ModelChoiceField(widget=forms.Select(attrs={  'class':'form-control'}),queryset = Categorie.objects.all(),required = True)
	groupe = forms.ModelChoiceField(widget=forms.Select(attrs={  'class':'form-control'}),queryset = Groupe.objects.filter(nb_mouton_acheter__gt=F('nb_mouton_vendu')),required = True)
	couleur = forms.CharField(widget=forms.Select(attrs={'class': 'form-control selectpicker'  } ,choices=choices ),required = True)
	photo = forms.ImageField(widget=forms.FileInput(attrs={'accept':"image/*" ,}), required = True)
	

	class Meta:
		model = Mouton
		fields = (
			'categorie',
			'groupe',
			'couleur',
			'photo',

			)

	def clean_groupe(self):
		data = self.cleaned_data['groupe']
		is_insert = self.instance.pk is None
		if not is_insert:
			etat = self.instance.etat
			if etat == 'Vendu' and  data != self.instance.groupe:
				raise forms.ValidationError("Groupe ne peut pas etre changer car ce mouton a ete vendu")
		return data


class EncaissementForm(forms.ModelForm):
	vente = forms.ModelChoiceField(widget=forms.Select(attrs={  'class':'form-control'}),queryset = Vente.objects.all(),required = True)
	client = forms.ModelChoiceField(widget=forms.Select(attrs={  'class':'form-control'}),queryset = Client.objects.all(),required = True)
	montant = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = Encaissement
		fields = (
			'vente',
			'client',
			'montant',
			)

class LigneVenteForm(forms.ModelForm):
	mouton = forms.ModelChoiceField(widget=forms.Select(attrs={  'class':'form-control'}),queryset = Mouton.objects.filter(etat="En Stock"),required = True)
	mt_vente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = LigneVente
		fields = (
			'mouton',
			'mt_vente',
			)

class VenteForm(forms.ModelForm):
	client = forms.ModelChoiceField(widget=forms.Select(attrs={  'class':'form-control'}),queryset = Client.objects.all(),required = True)

	class Meta:
		model = Vente
		fields = (
			'client',
			)
class FraisForm(forms.ModelForm):
	montant = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	designation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = Frais
		fields = (
			'montant',
			'designation',
			)