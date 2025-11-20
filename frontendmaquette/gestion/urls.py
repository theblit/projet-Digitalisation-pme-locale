from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stocks/', views.stocks, name='stocks'),
    path('ventes/', views.ventes, name='ventes'),
    path('achats/', views.achats, name='achats'),
    path('clients/', views.clients, name='clients'),
    path('rapports/', views.rapports, name='rapports'),
    path('produit/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('client/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('facture/ajouter/', views.ajouter_facture, name='ajouter_facture'),
    path('commande/ajouter/', views.ajouter_commande, name='ajouter_commande'),
    path('api/categories/', views.api_categories, name='api_categories'),
    path('api/categorie/ajouter/', views.api_ajouter_categorie, name='api_ajouter_categorie'),
    path('api/clients/', views.api_clients, name='api_clients'),
    path('api/client/ajouter/', views.api_ajouter_client, name='api_ajouter_client'),
    path('api/modes-paiement/', views.api_modes_paiement, name='api_modes_paiement'),
    path('api/mode-paiement/ajouter/', views.api_ajouter_mode_paiement, name='api_ajouter_mode_paiement'),
    path('api/fournisseurs/', views.api_fournisseurs, name='api_fournisseurs'),
    path('api/fournisseur/ajouter/', views.api_ajouter_fournisseur, name='api_ajouter_fournisseur'),
    path('api/statuts-facture/', views.api_statuts_facture, name='api_statuts_facture'),
    path('api/types-client/', views.api_types_client, name='api_types_client'),
    path('api/produits/', views.api_produits, name='api_produits'),
    path('api/facture/<int:facture_id>/lignes/', views.api_facture_lignes, name='api_facture_lignes'),
    path('api/fournisseurs/commandes/', views.api_fournisseurs_commandes, name='api_fournisseurs_commandes'),
]