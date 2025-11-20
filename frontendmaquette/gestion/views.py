from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produit, Client, Fournisseur, Facture, BonCommande, Categorie, ModePaiement, LigneFacture, LigneCommande
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import JsonResponse
import json


def dashboard(request):
    """Vue du tableau de bord"""
    # Statistiques
    total_produits = Produit.objects.count()
    produits_stock_faible = Produit.objects.filter(stock__lt=F('seuil')).count()
    total_clients = Client.objects.count()
    
    # Ventes du mois
    from datetime import datetime, timedelta
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_ventes_mois = Facture.objects.filter(date__gte=debut_mois).aggregate(
        total=Sum('montant')
    )['total'] or 0
    
    # Produits avec alerte
    alertes_stock = Produit.objects.filter(stock__lt=F('seuil')).order_by('stock')[:5]
    
    # Top produits - Les plus vendus (nombre de fois achetés)
    top_produits = Produit.objects.annotate(
        nombre_achats=Count('lignefacture')
    ).filter(nombre_achats__gt=0).order_by('-nombre_achats')[:5]
    
    context = {
        'total_produits': total_produits,
        'produits_stock_faible': produits_stock_faible,
        'total_clients': total_clients,
        'total_ventes_mois': total_ventes_mois,
        'alertes_stock': alertes_stock,
        'top_produits': top_produits,
    }
    return render(request, 'gestion/dashboard.html', context)


def stocks(request):
    """Vue de gestion des stocks"""
    # Recherche
    search_query = request.GET.get('search', '')
    
    if search_query:
        produits = Produit.objects.filter(
            Q(nom__icontains=search_query) | 
            Q(code__icontains=search_query) |
            Q(categorie__nom__icontains=search_query)
        )
    else:
        produits = Produit.objects.all()
    
    # Statistiques
    total_produits = Produit.objects.count()
    stock_faible = Produit.objects.filter(stock__lt=F('seuil')).count()
    stock_ok = Produit.objects.filter(stock__gte=F('seuil')).count()
    
    context = {
        'produits': produits,
        'total_produits': total_produits,
        'stock_faible': stock_faible,
        'stock_ok': stock_ok,
        'search_query': search_query,
    }
    return render(request, 'gestion/stocks.html', context)


def ventes(request):
    """Vue de gestion des ventes"""
    factures = Facture.objects.all().order_by('-date')
    
    context = {
        'factures': factures,
    }
    return render(request, 'gestion/ventes.html', context)


def achats(request):
    """Vue de gestion des achats"""
    commandes = BonCommande.objects.all().order_by('-date')
    fournisseurs = Fournisseur.objects.all()
    
    # Stats
    commandes_en_cours = commandes.filter(statut='en_cours').count()
    commandes_livrees = commandes.filter(statut='livree').count()
    total_achats_mois = commandes.aggregate(total=Sum('montant'))['total'] or 0
    total_fournisseurs = fournisseurs.count()
    
    context = {
        'commandes': commandes,
        'fournisseurs': fournisseurs,
        'commandes_en_cours': commandes_en_cours,
        'commandes_livrees': commandes_livrees,
        'total_achats_mois': total_achats_mois,
        'total_fournisseurs': total_fournisseurs,
    }
    return render(request, 'gestion/achats.html', context)


def clients(request):
    """Vue de gestion des clients"""
    # Recherche
    search_query = request.GET.get('search', '')
    
    if search_query:
        clients_list = Client.objects.filter(
            Q(nom__icontains=search_query) | 
            Q(telephone__icontains=search_query)
        )
    else:
        clients_list = Client.objects.all()
    
    # Statistiques
    total_clients = Client.objects.count()
    clients_pro = Client.objects.filter(type_client='professionnel').count()
    clients_particuliers = Client.objects.filter(type_client='particulier').count()
    total_credits = Client.objects.aggregate(total=Sum('credit_en_cours'))['total'] or 0
    
    # Top clients
    top_clients = Client.objects.order_by('-total_achats')[:5]
    
    context = {
        'clients': clients_list,
        'top_clients': top_clients,
        'total_clients': total_clients,
        'clients_pro': clients_pro,
        'clients_particuliers': clients_particuliers,
        'total_credits': total_credits,
        'search_query': search_query,
    }
    return render(request, 'gestion/clients.html', context)


def rapports(request):
    """Vue des rapports et analyses"""
    # KPIs
    ca = Facture.objects.aggregate(total=Sum('montant'))['total'] or 0
    nb_transactions = Facture.objects.count()
    panier_moyen = ca / nb_transactions if nb_transactions > 0 else 0
    
    # Marge brute
    total_achats = BonCommande.objects.aggregate(total=Sum('montant'))['total'] or 0
    marge_brute = ca - total_achats
    
    context = {
        'ca': ca,
        'marge_brute': marge_brute,
        'nb_transactions': nb_transactions,
        'panier_moyen': panier_moyen,
    }
    return render(request, 'gestion/rapports.html', context)


def ajouter_produit(request):
    """Ajouter un nouveau produit via AJAX"""
    if request.method == 'POST':
        try:
            code = request.POST.get('code')
            nom = request.POST.get('nom')
            categorie_id = request.POST.get('categorie')
            stock = request.POST.get('stock', 0)
            seuil = request.POST.get('seuil', 10)
            prix_unitaire = request.POST.get('prix_unitaire')
            
            categorie = Categorie.objects.get(id=categorie_id)
            
            produit = Produit.objects.create(
                code=code,
                nom=nom,
                categorie=categorie,
                stock=int(stock),
                seuil=int(seuil),
                prix_unitaire=float(prix_unitaire)
            )
            
            return JsonResponse({'success': True, 'message': 'Produit ajouté avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('gestion:stocks')


def ajouter_client(request):
    """Ajouter un nouveau client via AJAX"""
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom')
            type_client = request.POST.get('type_client')
            telephone = request.POST.get('telephone')
            
            client = Client.objects.create(
                nom=nom,
                type_client=type_client,
                telephone=telephone
            )
            
            return JsonResponse({'success': True, 'message': 'Client ajouté avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('gestion:clients')


def ajouter_commande(request):
    """Ajouter une nouvelle commande avec articles"""
    if request.method == 'POST':
        try:
            import json
            fournisseur_id = request.POST.get('fournisseur_id')
            livraison_prevue = request.POST.get('livraison_prevue')
            articles_str = request.POST.get('articles', '[]')
            
            if not fournisseur_id or not livraison_prevue:
                return JsonResponse({'success': False, 'error': 'Données manquantes'})
            
            # Parser les articles JSON
            articles = json.loads(articles_str)
            if not articles:
                return JsonResponse({'success': False, 'error': 'Aucun article n\'a été ajouté'})
            
            fournisseur = Fournisseur.objects.get(id=fournisseur_id)
            
            # Calculer le montant total
            montant_total = 0
            for article in articles:
                montant_total += float(article['sousTotal'])
            
            # Créer la commande
            numero_commande = f"BC-{BonCommande.objects.count() + 1:05d}"
            commande = BonCommande.objects.create(
                numero=numero_commande,
                fournisseur=fournisseur,
                montant=montant_total,
                livraison_prevue=livraison_prevue,
                statut='en_cours'
            )
            
            # Créer les lignes de commande
            for article in articles:
                produit = Produit.objects.get(id=article['id'])
                LigneCommande.objects.create(
                    commande=commande,
                    produit=produit,
                    quantite=article['quantity'],
                    prix_unitaire=article['price'],
                    sous_total=article['sousTotal']
                )
            
            return JsonResponse({
                'success': True,
                'message': f'Commande {numero_commande} créée avec succès',
                'id': commande.id
            })
        except Fournisseur.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Fournisseur non trouvé'})
        except Produit.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Produit non trouvé'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Erreur lors du traitement des articles'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('gestion:achats')


def api_categories(request):
    """API pour obtenir les catégories"""
    categories = Categorie.objects.all().values('id', 'nom')
    return JsonResponse({
        'categories': list(categories)
    })


def api_ajouter_categorie(request):
    """API pour ajouter une nouvelle catégorie"""
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom', '').strip()
            
            if not nom:
                return JsonResponse({'success': False, 'error': 'Le nom de la catégorie est requis'})
            
            categorie, created = Categorie.objects.get_or_create(nom=nom)
            
            if created:
                return JsonResponse({
                    'success': True,
                    'message': f'Catégorie "{nom}" ajoutée avec succès',
                    'id': categorie.id,
                    'nom': categorie.nom
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'La catégorie "{nom}" existe déjà'
                })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


def ajouter_facture(request):
    """Ajouter une nouvelle facture avec articles"""
    if request.method == 'POST':
        try:
            client_id = request.POST.get('client')
            mode_paiement_id = request.POST.get('mode_paiement')
            statut = request.POST.get('statut', 'en_attente')
            
            # Récupérer les articles JSON
            articles_json = request.POST.get('articles', '[]')
            articles = json.loads(articles_json)
            
            if not client_id or not mode_paiement_id or not articles:
                return JsonResponse({'success': False, 'error': 'Données manquantes'})
            
            client = Client.objects.get(id=client_id)
            mode_paiement = ModePaiement.objects.get(id=mode_paiement_id)
            
            # Calculer le montant total
            montant_total = 0
            for article in articles:
                montant_total += float(article['sous_total'])
            
            # Créer la facture
            numero_facture = f"FAC-{Facture.objects.count() + 1:05d}"
            facture = Facture.objects.create(
                numero=numero_facture,
                date=timezone.now(),
                client=client,
                montant=montant_total,
                mode_paiement=mode_paiement,
                statut=statut
            )
            
            # Mettre à jour le total achats du client
            client.total_achats += montant_total
            client.save()
            
            # Créer les articles
            for article in articles:
                produit = Produit.objects.get(id=article['produit_id'])
                LigneFacture.objects.create(
                    facture=facture,
                    produit=produit,
                    quantite=int(article['quantite']),
                    prix_unitaire=float(article['prix_unitaire']),
                    sous_total=float(article['sous_total'])
                )
            
            return JsonResponse({
                'success': True,
                'message': f'Facture {numero_facture} créée avec succès',
                'id': facture.id
            })
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Client non trouvé'})
        except ModePaiement.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mode de paiement non trouvé'})
        except Produit.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Produit non trouvé'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('gestion:ventes')



def api_clients(request):
    """API pour récupérer tous les clients avec nombre de factures"""
    clients = Client.objects.annotate(
        nombre_factures=Count('facture')
    ).values('id', 'nom', 'type_client', 'telephone', 'total_achats', 'credit_en_cours', 'nombre_factures')
    return JsonResponse({
        'clients': list(clients)
    })


def api_ajouter_client(request):
    """API pour ajouter un nouveau client"""
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom', '').strip()
            type_client = request.POST.get('type_client', 'particulier')
            telephone = request.POST.get('telephone', '').strip()
            
            if not nom:
                return JsonResponse({'success': False, 'error': 'Le nom du client est requis'})
            
            client = Client.objects.create(
                nom=nom,
                type_client=type_client,
                telephone=telephone,
                credit_en_cours=0,
                total_achats=0
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Client "{nom}" ajouté avec succès',
                'id': client.id,
                'nom': client.nom,
                'type_client': client.type_client,
                'telephone': client.telephone
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


def api_modes_paiement(request):
    """API pour récupérer tous les modes de paiement"""
    modes = ModePaiement.objects.all().values('id', 'nom', 'description')
    return JsonResponse({
        'modes': list(modes)
    })


def api_ajouter_mode_paiement(request):
    """API pour ajouter un nouveau mode de paiement"""
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom', '').strip()
            description = request.POST.get('description', '').strip()
            
            if not nom:
                return JsonResponse({'success': False, 'error': 'Le nom du mode de paiement est requis'})
            
            # Vérifier si le mode existe déjà
            mode_existant = ModePaiement.objects.filter(nom=nom).first()
            if mode_existant:
                return JsonResponse({
                    'success': False,
                    'error': f'Le mode de paiement "{nom}" existe déjà'
                })
            
            mode = ModePaiement.objects.create(
                nom=nom,
                description=description
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Mode de paiement "{nom}" ajouté avec succès',
                'id': mode.id,
                'nom': mode.nom,
                'description': mode.description
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


def api_fournisseurs(request):
    """API pour récupérer tous les fournisseurs"""
    fournisseurs = Fournisseur.objects.all().values('id', 'nom', 'contact', 'specialite')
    return JsonResponse({
        'fournisseurs': list(fournisseurs)
    })


def api_statuts_facture(request):
    """API pour récupérer les statuts de facture"""
    statuts = Facture.STATUT_CHOICES
    return JsonResponse({
        'statuts': [{'value': code, 'label': label} for code, label in statuts]
    })


def api_types_client(request):
    """API pour récupérer les types de client"""
    types = Client.TYPE_CHOICES
    return JsonResponse({
        'types': [{'value': code, 'label': label} for code, label in types]
    })


def api_ajouter_fournisseur(request):
    """API pour ajouter un nouveau fournisseur"""
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom', '').strip()
            contact = request.POST.get('contact', '').strip()
            specialite = request.POST.get('specialite', '').strip()
            
            if not nom or not contact or not specialite:
                return JsonResponse({'success': False, 'error': 'Tous les champs sont requis'})
            
            fournisseur = Fournisseur.objects.create(
                nom=nom,
                contact=contact,
                specialite=specialite,
                total_commandes_mois=0
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Fournisseur "{nom}" ajouté avec succès',
                'id': fournisseur.id,
                'nom': fournisseur.nom,
                'contact': fournisseur.contact,
                'specialite': fournisseur.specialite
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


def api_produits(request):
    """API pour récupérer tous les produits avec stock > 0"""
    produits = Produit.objects.filter(stock__gt=0).values(
        'id', 'code', 'nom', 'categorie_id', 'categorie__nom', 'prix_unitaire', 'stock'
    )
    return JsonResponse({
        'produits': list(produits)
    })


def api_fournisseurs_commandes(request):
    """API pour récupérer le nombre de commandes par fournisseur ce mois"""
    from django.utils import timezone
    from django.db.models import Q, Count
    
    today = timezone.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    fournisseurs = Fournisseur.objects.annotate(
        commandes_mois=Count(
            'boncommande',
            filter=Q(boncommande__date__gte=first_day_of_month)
        )
    ).values('id', 'nom', 'contact', 'specialite', 'commandes_mois')
    
    return JsonResponse({
        'success': True,
        'fournisseurs': list(fournisseurs)
    })


def api_facture_lignes(request, facture_id):
    """API pour récupérer les articles et détails complets d'une facture"""
    try:
        facture = Facture.objects.get(id=facture_id)
        lignes = facture.lignes.all().values(
            'id', 'produit__nom', 'produit__code', 'quantite', 'prix_unitaire', 'sous_total'
        )
        
        # Calculer le total des articles
        total_articles = sum(float(ligne['sous_total']) for ligne in lignes)
        
        return JsonResponse({
            'success': True,
            'facture': {
                'id': facture.id,
                'numero': facture.numero,
                'date': facture.date.strftime('%d/%m/%Y'),
                'montant': str(facture.montant),
                'montant_float': float(facture.montant),
                'client': facture.client.nom,
                'client_type': facture.client.get_type_client_display(),
                'client_telephone': facture.client.telephone,
                'mode_paiement': facture.mode_paiement.nom if facture.mode_paiement else '--',
                'statut': facture.statut,
                'statut_display': facture.get_statut_display()
            },
            'lignes': list(lignes),
            'total_articles': total_articles
        })
    except Facture.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Facture non trouvée'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    except Facture.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Facture non trouvée'}, status=404)