from django.urls import path
from shop.views import index, detailArticle

urlpatterns = [
    path('', index, name='home'),
    path('<int:myid>/', detailArticle, name='detailArticle'),
    
]