from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Commande  
from django.core.paginator import Paginator

def index(request):
    product_objects = Product.objects.all()

    item_name = request.GET.get('item-name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    # pour la pagination
    paginator = Paginator(product_objects, 2)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)
    
    return render(request, 'shop/index.html', {'product_objects': product_objects})


def detailArticle(request, myid):
    product = Product.objects.get(id=myid)
    return render(request, 'shop/detailArticle.html', {'product': product})
    
    
def checkout(request):
    if request.method == "POST":
        # CORRIGÉ: utiliser les minuscules pour correspondre au HTML
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        adress = request.POST.get('adress')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        
        # Créer la commande
        com = Commande(
            items=items,
            total=total,
            nom=nom,
            email=email,
            adress=adress,
            ville=ville,
            pays=pays,
            zipcode=zipcode
        )
        com.save()
        
        messages.success(request, 'Commande passée avec succès!')
        return redirect('home')
    
    return render(request, 'shop/checkout.html')