from django.urls import path
from shop.views import index, detailArticle, checkout

urlpatterns = [
    path('', index, name='home'),
    path('<int:myid>/', detailArticle, name='detailArticle'),
    path('checkout/', checkout, name='checkout'),
    
]