from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Commande, CodePromo, ProfilVendeur
from django.core.paginator import Paginator
from django.utils import timezone
import json; from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import InscriptionForm, ProfilVendeurForm, ProductForm




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







# Vue d'inscription
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ! Votre compte vendeur a été créé.')
            return redirect('mon_profil')
    else:
        form = InscriptionForm()
    
    return render(request, 'shop/inscription.html', {'form': form})


# Vue de connexion
def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bon retour {username} !')
                return redirect('home')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'shop/connexion.html', {'form': form})


# Vue de déconnexion
def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('home')


# Profil vendeur
@login_required
def mon_profil(request):
    try:
        profil = request.user.profil_vendeur
    except ProfilVendeur.DoesNotExist:
        # Créer un profil si n'existe pas
        profil = ProfilVendeur.objects.create(
            user=request.user,
            nom_boutique=f"Boutique de {request.user.username}",
            telephone=""
        )
    
    if request.method == 'POST':
        form = ProfilVendeurForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('mon_profil')
    else:
        form = ProfilVendeurForm(instance=profil)
    
    mes_produits = Product.objects.filter(vendeur=profil).order_by('-date_added')
    
    context = {
        'profil': profil,
        'form': form,
        'mes_produits': mes_produits
    }
    
    return render(request, 'shop/mon_profil.html', context)


# Ajouter un produit
@login_required
def ajouter_produit(request):
    try:
        profil = request.user.profil_vendeur
    except ProfilVendeur.DoesNotExist:
        messages.error(request, 'Vous devez d\'abord compléter votre profil vendeur.')
        return redirect('mon_profil')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.vendeur = profil
            produit.statut = 'en_attente'  # En attente de validation
            produit.save()
            messages.success(request, 'Produit ajouté avec succès ! Il sera visible après validation.')
            return redirect('mon_profil')
    else:
        form = ProductForm()
    
    return render(request, 'shop/ajouter_produit.html', {'form': form})


# Modifier un produit
@login_required
def modifier_produit(request, produit_id):
    produit = Product.objects.get(id=produit_id)
    
    # Vérifier que c'est bien le vendeur du produit
    if produit.vendeur.user != request.user:
        messages.error(request, 'Vous n\'avez pas la permission de modifier ce produit.')
        return redirect('mon_profil')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès !')
            return redirect('mon_profil')
    else:
        form = ProductForm(instance=produit)
    
    return render(request, 'shop/modifier_produit.html', {'form': form, 'produit': produit})


# Supprimer un produit
@login_required
def supprimer_produit(request, produit_id):
    produit = Product.objects.get(id=produit_id)
    
    # Vérifier que c'est bien le vendeur du produit
    if produit.vendeur.user != request.user:
        messages.error(request, 'Vous n\'avez pas la permission de supprimer ce produit.')
        return redirect('mon_profil')
    
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé avec succès !')
        return redirect('mon_profil')
    
    return render(request, 'shop/supprimer_produit.html', {'produit': produit})