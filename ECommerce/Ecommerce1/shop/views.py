from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Commande, CodePromo
from django.core.paginator import Paginator
from django.utils import timezone
import json

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
        telephone = request.POST.get('telephone')

        # Calculer les frais de livraison (exemple simple)
        frais_livraison = 1500 if ville.lower() != 'abidjan' else 500
        
        # Créer la commande temporaire (avant paiement)
        commande = Commande(
           items=items,
            nom=nom,
            email=email,
            adress=adress,
            ville=ville,
            pays=pays,
            zipcode=zipcode,
            telephone=telephone,
            sous_total=total,
            frais_livraison=frais_livraison,
            total=float(total) + frais_livraison,
            statut='en_attente'
        )
        commande.save()

       # Rediriger vers la page de paiement
        return redirect('paiement', commande_id=commande.id)
    
    return render(request, 'shop/checkout.html')
    
        
    
    

def paiement(request, commande_id):
    try:
        commande = Commande.objects.get(id=commande_id)
    except Commande.DoesNotExist:
        messages.error(request, 'Commande introuvable.')
        return redirect('home')
    
    if request.method == "POST":

        # Appliquer le code promo
        code_promo = request.POST.get('code_promo')
        if code_promo:
            try:
                promo = CodePromo.objects.get(code=code_promo)
                if promo.est_valide():
                    if promo.reduction_pourcentage > 0:
                        commande.reduction = commande.sous_total * (promo.reduction_pourcentage / 100)
                    else:
                        commande.reduction = promo.reduction_montant
                    
                    commande.code_promo = code_promo
                    commande.total = commande.sous_total + commande.frais_livraison - commande.reduction
                    commande.save()
                    
                    promo.utilisations_actuelles += 1
                    promo.save()
                    
                    messages.success(request, f'Code promo appliqué ! Réduction de {commande.reduction} XOF')
                else:
                    messages.error(request, 'Code promo invalide ou expiré.')
            except CodePromo.DoesNotExist:
                messages.error(request, 'Code promo introuvable.')
            
            return redirect('paiement', commande_id=commande.id)
        
        # Traiter le paiement
        methode_paiement = request.POST.get('methode_paiement')
        commande.methode_paiement = methode_paiement
        
        if methode_paiement == 'mobile_money':
            # Logique Mobile Money (à implémenter avec l'API de votre opérateur)
            commande.statut = 'paye'
            commande.date_paiement = timezone.now()
            commande.save()
            messages.success(request, 'Paiement Mobile Money effectué avec succès !')
            return redirect('confirmation', commande_id=commande.id)
        
        elif methode_paiement == 'especes':
            commande.statut = 'en_attente'
            commande.save()
            messages.success(request, 'Commande enregistrée ! Paiement à la livraison.')
            return redirect('confirmation', commande_id=commande.id)
        
        # Autres méthodes de paiement à implémenter
    
    # Charger le panier depuis les items
    try:
        panier = json.loads(commande.items)
    except:
        panier = {}
    
    context = {
        'commande': commande,
        'panier': panier
    }
    
    return render(request, 'shop/paiement.html', context)


def confirmation(request, commande_id):
    try:
        commande = Commande.objects.get(id=commande_id)
    except Commande.DoesNotExist:
        messages.error(request, 'Commande introuvable.')
        return redirect('home')
    
    return render(request, 'shop/confirmation.html', {'commande': commande})