from django.contrib import admin
from django.urls import path , re_path
from .views import *
urlpatterns = [
    path('', dashboard , name='dashboard'),
    path('ventes/', tous_ventes , name='tous_ventes'),
    path('ajouter-ventes/', ajouter_vente , name='ajouter_vente'),
    re_path(r'detail-vente/(?P<pk>[\w-]+)/', vente_detail , name='vente_detail'),

    path('ajouter-categorie/', ajouter_categorie , name='ajouter_categorie'),
    re_path(r'modifier-categorie/(?P<pk>[\w-]+)/', modifier_categorie , name='modifier_categorie'),
    re_path(r'supprimer-categorie/(?P<pk>[\w-]+)/', supprimer_categorie , name='supprimer_categorie'),
    path('categorie/', tous_categories , name='tous_categories'),
    
    path('ajouter-groupe/', ajouter_groupe , name='ajouter_groupe'),
    re_path(r'modifier-groupe/(?P<pk>[\w-]+)/', modifier_groupe , name='modifier_groupe'),
    re_path(r'supprimer-groupe/(?P<pk>[\w-]+)/', supprimer_groupe , name='supprimer_groupe'),
    path('groupe/', tous_groupes , name='tous_groupes'),

    path('ajouter-client/', ajouter_client , name='ajouter_client'),
    re_path(r'modifier-client/(?P<pk>[\w-]+)/', modifier_client , name='modifier_client'),
    re_path(r'supprimer-client/(?P<pk>[\w-]+)/', supprimer_client , name='supprimer_client'),
    path('client/', tous_clients , name='tous_clients'),

    path('ajouter-mouton/', ajouter_mouton , name='ajouter_mouton'),
    re_path(r'modifier-mouton/(?P<pk>[\w-]+)/', modifier_mouton , name='modifier_mouton'),
    re_path(r'supprimer-mouton/(?P<pk>[\w-]+)/', supprimer_mouton , name='supprimer_mouton'),
    path('mouton/', tous_moutons , name='tous_moutons'),

    path('ajouter-encaissement/', ajouter_encaissement , name='ajouter_encaissement'),
    re_path(r'annuler-encaissement/(?P<pk>[\w-]+)/', annuler_encaissement , name='annuler_encaissement'),
    path('encaissement/', tous_encaissements , name='tous_encaissements'),
    
    path('ajouter-frais/', ajouter_frais , name='ajouter_frais'),
    re_path(r'modifier-frais/(?P<pk>[\w-]+)/', modifier_frais , name='modifier_frais'),
    path('tous-frais/', tous_frais , name='tous_frais'),

    path('groups-stat/', groups_stat , name='groups_stat'),
]
