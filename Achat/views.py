from django.shortcuts import render , redirect , get_object_or_404
from django.contrib 				import messages

from .models import *
from .forms import *
from django.http                    import HttpResponse
import json 

# Create your views here.
def dashboard(request):
	template_name = 'dashboard.html'

	total_encissement = Encaissement.total_encissement()
	total_achat_mouton = Groupe.total_achat_mouton()
	total_nb_mouton = Groupe.total_nb_mouton()
	total_frais = Frais.total_frais()
	total_vente = Vente.total_vente()
	total_mouton_vendu = Vente.total_mouton_vendu()
	mouton_non_vendu = total_nb_mouton - total_mouton_vendu
	rest_a_payer = total_vente - total_encissement
	data = [1,2,3,4,5]
	args = {
		"total_encissement" :total_encissement,
		"total_achat_mouton" :total_achat_mouton,
		"total_nb_mouton" :total_nb_mouton,
		"total_mouton_vendu" :total_mouton_vendu,
		"mouton_non_vendu" :mouton_non_vendu,
		"total_frais" :total_frais,
		"rest_a_payer" :rest_a_payer,
		"data" :data,
	}
	return render(request , template_name, args)


def tous_ventes(request):
	template_name = 'tous_ventes.html'
	ventes = Vente.objects.all()
	args = {
		'ventes':ventes,
	}
	return render(request , template_name, args)



def ajouter_vente(request):
	template_name = 'ajouter_vente.html'
	vente_form = VenteForm()
	lignevente_form = LigneVenteForm()

	if request.method=='POST':
		if 'client_form' in request.POST:
			client_form = ClientForm(request.POST or None)
			if client_form.is_valid():
				try:
					client_form.save()
					messages.success(request , 'client a bien été ajouté')
				except Exception as e:
					messages.error(request , 'client n\'a pas été ajouté')

		if 'vente_form' in request.POST:
			vente_form = VenteForm(request.POST or None )
			moutons = request.POST.getlist('mouton')
			montants = request.POST.getlist('mt_vente')

			if  vente_form.is_valid():
				try:
					vente = vente_form.save()

					for i in range(len(moutons)):
						exists = LigneVente.verif_mouton(moutons[i])
						lignevente = LigneVente()
						mouton = get_object_or_404(Mouton , pk=moutons[i])
						if exists:
							messages.error(request , f'Vente annuler : Le Mouton N° {moutons[i]} a déja  été vendu ')
						else:
							lignevente.vente = vente
							lignevente.mouton = mouton
							lignevente.mt_vente = int(montants[i])
							lignevente.save()
					messages.success(request , 'Vente a bien été ajouté')
				except Exception as e:
					messages.error(request , f'Vente n\' pas été ajouté {e}')
				return redirect('tous_ventes')
		if 'mouton_form' in request.POST:
			mouton_form = MoutonForm(request.POST or None ,  request.FILES or None)
			if mouton_form.is_valid():
				try:
					mouton_form.save()
					messages.success(request , 'Mouton a bien été ajouté')

				except Exception as e:
					messages.error(request , 'Mouton n\'a pas été ajouté')
	


	mouton_form = MoutonForm()
	client_form = ClientForm()
	
	args = {
		'vente_form':vente_form,
		'lignevente_form':lignevente_form,
		'mouton_form':mouton_form,
		'client_form':client_form,
	}
	return render(request , template_name , args)



def ajouter_categorie(request):
	template_name = "ajouter_modifier_categorie.html"
	form = CategorieForm()
	if request.method =="POST":
		form = CategorieForm(request.POST)
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'Categorie a bien été Ajouté')
			except Exception as e:
				messages.error(request , 'Categorie n\'a pas été ajouté')
			return redirect('tous_categories')


	args = {'form':form}
	return render(request , template_name , args)


def modifier_categorie(request , pk):
	template_name = "ajouter_modifier_categorie.html"
	instance = get_object_or_404(Categorie , pk=pk)
	form = CategorieForm(request.POST or None,instance=instance)
	if request.method =="POST":
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'Categorie a bien été modifié')
				return redirect('tous_categories')
			except Exception as e:
				messages.error(request , 'Categorie n\'a pas été modifié')
	args = {'form':form}
	return render(request , template_name , args)


	args = {'form':form}
	return render(request , template_name , args)


def supprimer_categorie(request , pk):
	instance = get_object_or_404(Categorie , pk=pk)
	try:
		instance.delete()
		messages.success(request , 'La categorie a bien été supprimer')
		return redirect('tous_categories')
	except Exception as e:
		messages.error(request , 'La categorie n\'a pas été supprimer {}'.format(e))
		return redirect('tous_categories')


	args = {'form':form}
	return render(request , template_name , args)



def tous_categories(request):
	template_name = 'tous_categories.html'
	categories = Categorie.objects.all()
	print(categories)
	args = {'categories':categories}
	return render(request , template_name , args)


def ajouter_groupe(request):
	template_name = "ajouter_modifier_groupe.html"
	form = GroupeForm()
	if request.method =="POST":
		form = GroupeForm(request.POST or None)
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'Groupe a bien été ajouté')
			except Exception as e:
				messages.error(request , 'Groupe n\'a pas été ajouté')

			return redirect('tous_groupes')


	args = {'form':form}
	return render(request , template_name , args)

def vente_detail(request , pk):
	template_name = 'detail_vente.html'
	vente = get_object_or_404(Vente , pk=pk)
	ligneventes = LigneVente.objects.filter(vente=vente)
	encaissements = Encaissement.objects.filter(vente=vente)
	args = {
		'vente':vente,
		'ligneventes':ligneventes,
		'encaissements':encaissements,
	}

	return render(request ,template_name , args)
def modifier_groupe(request , pk):
	template_name = "ajouter_modifier_groupe.html"
	instance = get_object_or_404(Groupe , pk=pk)
	form = GroupeForm(request.POST or None,instance=instance)
	if request.method =="POST":
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'Groupe a bien été modifié')
				return redirect('tous_groupes')
			except Exception as e:
				messages.error(request , 'Groupe n\'a pas été modifié')
	args = {'form':form}
	return render(request , template_name , args)


	args = {'form':form}
	return render(request , template_name , args)


def supprimer_groupe(request , pk):
	instance = get_object_or_404(Groupe , pk=pk)
	try:
		instance.delete()
		messages.success(request , 'Le Groupe a bien été supprimer')
		return redirect('tous_groupes')
	except Exception as e:
		messages.error(request , 'Le Groupe n\'a pas été supprimer {}'.format(e))
		return redirect('tous_groupes')


	args = {'form':form}
	return render(request , template_name , args)



def tous_groupes(request):
	template_name = 'tous_groupes.html'
	groupes = Groupe.objects.all()
	args = {'groupes':groupes}
	return render(request , template_name , args)

def ajouter_client(request):
	template_name = "ajouter_modifier_client.html"
	form = ClientForm()
	if request.method =="POST":
		form = ClientForm(request.POST)
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'client a bien été ajouté')
			except Exception as e:
				raise e
				messages.error(request , 'client n\'a pas été ajouté')
			return redirect('tous_clients')


	args = {'form':form}
	return render(request , template_name , args)


def modifier_client(request , pk):
	template_name = "ajouter_modifier_client.html"
	instance = get_object_or_404(Client , pk=pk)
	form = ClientForm(request.POST or None,instance=instance)
	if request.method =="POST":
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'client a bien été modifié')
				return redirect('tous_clients')
			except Exception as e:
				messages.error(request , 'client n\'a pas été modifié')
	args = {'form':form}
	return render(request , template_name , args)


	args = {'form':form}
	return render(request , template_name , args)


def supprimer_client(request , pk):
	instance = get_object_or_404(Client , pk=pk)
	encaissement = Encaissement.objects.filter(client=instance).exists()
	vente = Vente.objects.filter(client=instance).exists()
	if encaissement:
		messages.error(request , 'Ce client ne peut pas être supprimé car il a des encaissements non remboursés')
	elif vente:
		messages.error(request , 'Ce client ne peut pas être supprimé car il a des vente non annulées')
	else:
		try:
			instance.delete()
			messages.success(request , 'La client a bien été supprimer')
		except Exception as e:
			messages.error(request , 'La client n\'a pas été supprimer {}'.format(e))


	return redirect('tous_clients')



def tous_clients(request):
	template_name = 'tous_clients.html'
	clients = Client.objects.all()
	args = {'clients':clients}
	return render(request , template_name , args)




def ajouter_mouton(request):
	template_name = "ajouter_modifier_mouton.html"
	form = MoutonForm()
	if request.method =="POST":
		form = MoutonForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'mouton a bien été ajouté')
			except Exception as e:
				raise e
				messages.error(request , 'mouton n\'a pas été ajouté')
			return redirect('tous_moutons')


	args = {'form':form}
	return render(request , template_name , args)


def modifier_mouton(request , pk):
	template_name = "ajouter_modifier_mouton.html"
	instance = get_object_or_404(Mouton , pk=pk)
	form = MoutonForm(request.POST or None, request.FILES or None,instance=instance)
	if request.method =="POST":
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'mouton a bien été modifié')
				return redirect('tous_moutons')
			except Exception as e:
				messages.error(request , 'mouton n\'a pas été modifié')
	args = {'form':form}
	return render(request , template_name , args)


	args = {'form':form}
	return render(request , template_name , args)


def supprimer_mouton(request , pk):
	instance = get_object_or_404(Mouton , pk=pk)
	exists = LigneVente.verif_mouton(pk)
	if exists:
		messages.error(request , 'Ce mouton ne peut pas être supprimé car il a été vendu')
	else:
		try:
			instance.delete()
			messages.success(request , 'La mouton a bien été supprimer')
		except Exception as e:
			messages.error(request , 'La mouton n\'a pas été supprimer {}'.format(e))


	return redirect('tous_moutons')



def tous_moutons(request):
	template_name = 'tous_moutons.html'
	moutons = Mouton.objects.all()
	args = {'moutons':moutons}
	return render(request , template_name , args)





def ajouter_encaissement(request):
	template_name = "ajouter_encaissement.html"
	form = EncaissementForm()
	if request.method =="POST":
		form = EncaissementForm(request.POST or None)
		if form.is_valid():
			try:
				instance = form.save(commit=False)
				valid = instance.verif_montant_encais()
				if valid:
					instance.save()
				else:
					messages.error(request , f'Montant non valid il reste seulement {instance.rest_a_encaisser} DA a encaisser')
				return redirect('ajouter_encaissement')

				messages.success(request , 'encaissement a bien été ajouté')
			except Exception as e:
				raise e
				messages.error(request , 'encaissement n\'a pas été ajouté')
			return redirect('tous_encaissements')


	args = {'form':form}
	return render(request , template_name , args)

def tous_encaissements(request):
	template_name = 'tous_encaissements.html'
	encaissements = Encaissement.objects.all()
	args = {'encaissements':encaissements}
	return render(request , template_name , args)

def annuler_encaissement(request , pk):
	instance = get_object_or_404(Encaissement , pk=pk)

	try:
		instance.annul_encais()
		instance.save()
		messages.success(request , 'L\' encaissement a bien été annuler')
	except Exception as e:
		messages.error(request , 'L\' encaissement n\'a pas été annuler {}'.format(e))


	return redirect('tous_encaissements')



def ajouter_frais(request):
	template_name = 'ajouter_modifier_frais.html'
	form = FraisForm()
	if request.method == 'POST':
		form = FraisForm(request.POST or None)
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'Frais a bien été Ajouté')
			except Exception as e:
				messages.error(request , 'Frais n\'a pas été Ajouté {}'.format(e))
			return redirect('tous_frais')

	args = {
		'form':form,
	}
	return render(request , template_name , args)

def tous_frais(request):
	template_name = 'tous_frais.html'
	
	frais = Frais.objects.all()
	args = {
		'frais':frais,
	}
	return render(request , template_name , args)



def modifier_frais(request , pk):
	template_name = "ajouter_modifier_frais.html"
	instance = get_object_or_404(Frais , pk=pk)
	form = FraisForm(request.POST or None, instance=instance)
	if request.method =="POST":
		if form.is_valid():
			try:
				form.save()
				messages.success(request , 'Frais a bien été modifié')
				return redirect('tous_frais')
			except Exception as e:
				messages.error(request , 'Frais n\'a pas été modifié')
	args = {'form':form}
	return render(request , template_name , args)


def groups_stat(request):

	groups = Groupe.objects.all()
	nom_groups = []
	acheter = []
	vendu = []
	for group in groups:
		nom_groups.append(group.designation)
		acheter.append(group.nb_mouton_acheter)
		vendu.append(group.nb_mouton_vendu)
	data = dict(
		nom_groups =nom_groups,
		acheter =acheter,
		vendu = vendu
		)
	json_data =  json.dumps(data)
	return HttpResponse(json_data,  content_type="application/json")
