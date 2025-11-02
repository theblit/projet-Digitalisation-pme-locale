from django.urls import path
from shop.views import (
    index, detailArticle, checkout, paiement, confirmation,
    inscription, connexion, deconnexion, mon_profil,
    ajouter_produit, modifier_produit, supprimer_produit
)

urlpatterns = [
    path('', index, name='home'),
    path('<int:myid>/', detailArticle, name='detailArticle'),
    path('checkout/', checkout, name='checkout'),
    path('paiement/<int:commande_id>/', paiement, name='paiement'),
    path('confirmation/<int:commande_id>/', confirmation, name='confirmation'),
    
    # Authentification
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    
    # Espace vendeur
    path('mon-profil/', mon_profil, name='mon_profil'),
    path('ajouter-produit/', ajouter_produit, name='ajouter_produit'),
    path('modifier-produit/<int:produit_id>/', modifier_produit, name='modifier_produit'),
    path('supprimer-produit/<int:produit_id>/', supprimer_produit, name='supprimer_produit'),
]