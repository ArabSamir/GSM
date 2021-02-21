categorie
	designation
	description

groupe
	designation
	nb_mouton_acheter
	nb_mouton_vendu
	prix_achat
	date_achat
	lieux_achat

	def update nb_mouton_vendu

mouton
	categorie
	groupe
	etat
	num
	couleur
	photo

client
	nom
	prenom
	adresse
	tel
	email
	num_cart
	date_ajout

ligne_vente
	mouton
	vente
	prix_vente

vente
	num
	client
	date_vente
	nb_mouton
	prix totale (addition des prix de vente de chaque mouton)

	signal update_etat_mouton

encaissement
	num_encaissement
	vente
	client
	montant
	date_encaissement
	description

	def calc_total_enc_par_ventew



create form
create template
create view insert
create view update
create view delete
create url
pour vente