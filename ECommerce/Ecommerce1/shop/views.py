from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    product_objects = Product.objects.all()

    item_name = request.GET.get('item-name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    # pour la pagination
    paginator = Paginator(product_objects, 2)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    
    return render(request, 'shop/index.html', {'product_objects': product_objects })


def detailArticle(request, myid):
    product = Product.objects.get(id=myid)
    return render(request, 'shop/detailArticle.html', {'product': product })
    
    