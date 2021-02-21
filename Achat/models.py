from django.db import models
from django.db.models.signals import post_save , pre_save , pre_delete
from django.shortcuts import  get_object_or_404
from django.shortcuts import  redirect
from django.contrib 				import messages

# Create your models here.

class Groupe(models.Model):
	designation = models.CharField(max_length=250, null=True,blank=True)
	nb_mouton_acheter = models.IntegerField(default = 0 ,null=True,blank=True )
	nb_mouton_vendu = models.IntegerField(default = 0 ,null=True,blank=True ) 
	prix_achat = models.IntegerField(default = 0 ,null=True,blank=True )
	date_achat =  models.DateField()
	lieux_achat =  models.CharField(max_length=250, null=True,blank=True)
	
	def update_nb_mouton_vendu_more(self ):
		self.nb_mouton_vendu += 1

	def update_nb_mouton_vendu_less(self):
		self.nb_mouton_vendu -= 1

	@property
	def prix_achat_total(self ):
		prix_total = self.nb_mouton_acheter * self.prix_achat

		return prix_total

	@property
	def rest_mouton(self):
		rest = self.nb_mouton_acheter- self.nb_mouton_vendu
		return rest
	
	def total_achat_mouton():
		groups = Groupe.objects.all()
		total = 0
		for groupe in groups:
			total = total + groupe.prix_achat* groupe.nb_mouton_acheter
		return total

	def total_nb_mouton():
		groups = Groupe.objects.all()
		total = 0
		for groupe in groups:
			total = total +  groupe.nb_mouton_acheter
		return total
	def __str__(self):
		return f'{self.designation} {self.date_achat}' 

class Categorie(models.Model):
	designation = models.CharField(max_length=250, null=True,blank=True)
	description = models.CharField(max_length=250, null=True,blank=True)

	def __str__(self):
		return self.designation 


class Mouton(models.Model):
	num = models.IntegerField(null=True,blank=True)
	categorie  = models.ForeignKey(Categorie , on_delete=models.SET_NULL,default= 1 , null = True, blank=True)
	groupe  = models.ForeignKey(Groupe , on_delete=models.SET_NULL,  null = True, blank=True)
	etat = models.CharField(default = 'En Stock',max_length=250, null=True,blank=True)
	couleur = models.CharField(max_length=250, null=True,blank=True)
	photo = models.ImageField(upload_to='photos/mouton' , blank=True )
	
	def modif_etat_vendu(self):
		self.etat = "Vendu"

	def modif_etat_ensotck(self):
		self.etat = "En Stock"

	def __str__(self):
		return f'{self.pk}'


class Client(models.Model):
	nom = models.CharField(max_length=250, null=True,blank=True)
	prenom = models.CharField(max_length=250, null=True,blank=True)
	adresse = models.CharField(max_length=250, null=True,blank=True)
	tel = models.CharField(max_length=250, null=True,blank=True)
	email = models.CharField(max_length=250, null=True,blank=True)
	date_ajout =  models.DateField(auto_now_add= True, null=True,blank=True)
	def __str__(self):
		return f'{self.nom} {self.prenom}'

class Vente(models.Model):

	client  = models.ForeignKey(Client , on_delete=models.SET_NULL, null = True, blank=True)
	date_vente =  models.DateField(auto_now_add= True, null=True,blank=True)
	nb_mouton_vendu = models.IntegerField(default = 0 ,null=True,blank=True ) 
	prix_vente_totale = models.IntegerField(default = 0 ,null=True,blank=True ) 
	# mouton 			= models.ManyToManyField(Mouton ,blank=True	)

	def total_vente():
		ventes = Vente.objects.all()
		total = 0
		for vente in ventes:
			total = total + vente.prix_vente_totale
		return total

	def total_mouton_vendu():
		ventes = Vente.objects.all()
		total = 0
		for vente in ventes:
			total = total + vente.nb_mouton_vendu
		return total

	def update_nb_mouton_vendu_more(self ):
		self.nb_mouton_vendu += 1

	def update_nb_mouton_vendu_less(self):
		self.nb_mouton_vendu -= 1

	def __str__(self):
		return f'{self.pk} {self.client}'


class LigneVente(models.Model):
	vente  = models.ForeignKey(Vente , on_delete=models.CASCADE, null = True, blank=True)
	mouton  = models.ForeignKey(Mouton , on_delete=models.CASCADE, null = True, blank=True)
	mt_vente = models.IntegerField(default = 0 ,null=True,blank=True )

	def verif_mouton(pk):
		mouton = get_object_or_404(Mouton , pk=pk)
		exists = LigneVente.objects.filter(mouton=mouton).exists()
		return  exists

	class Meta:
		unique_together = (("vente", "mouton"),)

def upd_prix_totale_vente_nb_mouton_vendu_more(sender , instance , **kwargs):
	vente = instance.vente
	group = instance.mouton.groupe
	group.update_nb_mouton_vendu_more()
	group.save()
	vente.prix_vente_totale = vente.prix_vente_totale+ instance.mt_vente
	vente.update_nb_mouton_vendu_more()
	vente.save()
	mouton = instance.mouton
	mouton.modif_etat_vendu()
	mouton.save()
post_save.connect(upd_prix_totale_vente_nb_mouton_vendu_more , sender=LigneVente)


def upd_prix_totale_vente_nb_mouton_vendu_less(sender , instance , **kwargs):
	vente = instance.vente
	group = instance.mouton.groupe
	group.update_nb_mouton_vendu_less()
	group.save()
	vente.prix_vente_totale = vente.prix_vente_totale- instance.mt_vente
	vente.update_nb_mouton_vendu_less()
	vente.save()
	mouton = instance.mouton
	mouton.modif_etat_ensotck()
	mouton.save()

pre_delete.connect(upd_prix_totale_vente_nb_mouton_vendu_less , sender=LigneVente)


class Encaissement(models.Model):
	vente  = models.ForeignKey(Vente , on_delete=models.CASCADE, null = True, blank=True)
	client  = models.ForeignKey(Client , on_delete=models.CASCADE, null = True, blank=True)
	montant = models.IntegerField(default = 0 ,null=True,blank=True )
	date_enc =  models.DateField(auto_now_add= True, null=True,blank=True)
	etat_enc = models.CharField(default = "E", max_length=20, null=True,blank=True)
	
	@property
	def total_enc_par_vente(self):
		encais = Encaissement.objects.filter(vente=self.vente)
		total_enc = 0
		if encais :
			for e in encais:
				if e.etat_enc == "E":
					total_enc = total_enc + e.montant
		return total_enc

	@property
	def rest_a_encaisser(self):
		rest = self.vente.prix_vente_totale - self.total_enc_par_vente
		return rest

	def verif_montant_encais(self):
		 

		if (self.rest_a_encaisser-self.montant) >= 0:
			return True
		else:
			return False

	def annul_encais(self):
		self.etat_enc = "A"
	
	def total_encissement():
		encais = Encaissement.objects.filter(etat_enc='E')
		total = 0
		for e in encais:
			total = total + e.montant
		return total

# def verif_montant(sender , instance , **kwargs):
# 	valid = instance.verif_montant_encais()
# 	if not valid:
# 		message = f'Montant non valid il rest seulment {instance.rest_a_encaisser} a encaisser'
# 		return  redirect('ajouter_encaissement')
# pre_save.connect(verif_montant , sender=Encaissement)


class Frais(models.Model):
	montant = models.IntegerField(default = 0 ,null=True,blank=True )
	designation = models.CharField(max_length=250, null=True,blank=True)
	date_sortie =  models.DateField(auto_now_add= True, null=True,blank=True)
	
	def total_frais():
		frais = Frais.objects.all()
		total = 0
		for f in frais:
			total = total + f.montant
		return total

	def __str__(self):
		return f'{date_sortie}'