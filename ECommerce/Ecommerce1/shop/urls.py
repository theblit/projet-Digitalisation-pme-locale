from django.urls import path
from shop.views import index, detailArticle, checkout, confirmation, paiement

urlpatterns = [
    path('', index, name='home'),
    path('<int:myid>/', detailArticle, name='detailArticle'),
    path('checkout/', checkout, name='checkout'),
       path('paiement/<int:commande_id>/', paiement, name='paiement'),
     path('confirmation/<int:commande_id>/', confirmation, name='confirmation'),
]