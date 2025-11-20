from django.contrib import admin
from django.utils.html import format_html
from .models import Categorie, Produit, Client, Fournisseur, Facture, BonCommande, ModePaiement, LigneFacture, LigneCommande


# ========== ADMIN PERSONNALISÉ ==========

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nombre_produits', 'date_creation']
    search_fields = ['nom']
    readonly_fields = ['date_creation']
    ordering = ['-date_creation']
    
    def nombre_produits(self, obj):
        count = obj.produit_set.count()
        return format_html(f'<span style="color: #417690; font-weight: bold;">{count}</span>')
    nombre_produits.short_description = 'Produits'


@admin.register(ModePaiement)
class ModePaiementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description', 'nombre_factures', 'date_creation']
    search_fields = ['nom']
    readonly_fields = ['date_creation']
    ordering = ['-date_creation']
    
    def nombre_factures(self, obj):
        count = obj.facture_set.count()
        return format_html(f'<span style="color: #417690;">{count} facture(s)</span>')
    nombre_factures.short_description = 'Utilisé dans'


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'categorie', 'prix_unitaire_display', 'stock_display', 'seuil', 'statut_stock_display', 'date_ajout']
    list_filter = ['categorie', 'date_ajout', 'stock']
    search_fields = ['nom', 'code', 'categorie__nom']
    list_per_page = 50
    readonly_fields = ['date_ajout']
    fieldsets = (
        ('Informations Produit', {
            'fields': ('code', 'nom', 'categorie')
        }),
        ('Gestion Stock', {
            'fields': ('stock', 'seuil')
        }),
        ('Prix', {
            'fields': ('prix_unitaire',)
        }),
        ('Dates', {
            'fields': ('date_ajout',),
            'classes': ('collapse',)
        }),
    )
    
    def prix_unitaire_display(self, obj):
        return format_html(f'<span style="color: #28a745; font-weight: bold;">{obj.prix_unitaire} FCFA</span>')
    prix_unitaire_display.short_description = 'Prix Unitaire'
    
    def stock_display(self, obj):
        if obj.stock == 0:
            color = '#dc3545'
            text = 'RUPTURE'
        elif obj.stock < obj.seuil * 0.5:
            color = '#fd7e14'
            text = 'CRITIQUE'
        elif obj.stock < obj.seuil:
            color = '#ffc107'
            text = 'FAIBLE'
        else:
            color = '#28a745'
            text = 'OK'
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.stock} ({text})</span>')
    stock_display.short_description = 'Stock'
    
    def statut_stock_display(self, obj):
        statut = obj.statut_stock()
        colors = {'critique': '#dc3545', 'faible': '#ffc107', 'ok': '#28a745'}
        color = colors.get(statut, '#6c757d')
        return format_html(f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{statut.upper()}</span>')
    statut_stock_display.short_description = 'Statut'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_client_display', 'telephone', 'total_achats_display', 'credit_en_cours_display', 'nombre_factures', 'date_creation']
    list_filter = ['type_client', 'date_creation']
    search_fields = ['nom', 'telephone']
    readonly_fields = ['date_creation', 'date_modification']
    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('nom', 'type_client', 'telephone')
        }),
        ('Historique Achat', {
            'fields': ('total_achats', 'credit_en_cours')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def type_client_display(self, obj):
        colors = {'particulier': '#417690', 'professionnel': '#6f42c1'}
        color = colors.get(obj.type_client, '#6c757d')
        label = obj.get_type_client_display()
        return format_html(f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{label}</span>')
    type_client_display.short_description = 'Type'
    
    def total_achats_display(self, obj):
        return format_html(f'<span style="color: #28a745; font-weight: bold;">{obj.total_achats} FCFA</span>')
    total_achats_display.short_description = 'Total Achats'
    
    def credit_en_cours_display(self, obj):
        color = '#dc3545' if obj.credit_en_cours > 0 else '#28a745'
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.credit_en_cours} FCFA</span>')
    credit_en_cours_display.short_description = 'Crédit en Cours'
    
    def nombre_factures(self, obj):
        count = obj.facture_set.count()
        color = '#417690' if count > 0 else '#6c757d'
        return format_html(f'<span style="color: {color}; font-weight: bold;">{count}</span>')
    nombre_factures.short_description = 'Factures'


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'contact', 'specialite', 'total_commandes_display', 'nombre_commandes', 'date_creation']
    list_filter = ['date_creation', 'specialite']
    search_fields = ['nom', 'specialite', 'contact']
    readonly_fields = ['date_creation', 'date_modification']
    fieldsets = (
        ('Informations Fournisseur', {
            'fields': ('nom', 'contact', 'specialite')
        }),
        ('Commandes', {
            'fields': ('total_commandes_mois',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def total_commandes_display(self, obj):
        return format_html(f'<span style="color: #28a745; font-weight: bold;">{obj.total_commandes_mois} FCFA</span>')
    total_commandes_display.short_description = 'Total Commandes Mois'
    
    def nombre_commandes(self, obj):
        count = obj.boncommande_set.count()
        return format_html(f'<span style="color: #417690; font-weight: bold;">{count}</span>')
    nombre_commandes.short_description = 'Commandes'


class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1
    fields = ['produit', 'quantite', 'prix_unitaire', 'sous_total']
    readonly_fields = ['sous_total']
    can_delete = True



@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date', 'client_display', 'montant_display', 'mode_paiement_display', 'statut_display']
    list_filter = ['statut', 'mode_paiement', 'date']
    search_fields = ['numero', 'client__nom']
    date_hierarchy = 'date'
    readonly_fields = ['date', 'numero', 'montant_total_display']
    fieldsets = (
        ('Informations Facture', {
            'fields': ('numero', 'date', 'client', 'mode_paiement', 'statut')
        }),
        ('Montant', {
            'fields': ('montant', 'montant_total_display'),
            'classes': ('collapse',)
        }),
    )
    inlines = [LigneFactureInline]
    
    def client_display(self, obj):
        type_label = obj.client.get_type_client_display()
        return format_html(f'<strong>{obj.client.nom}</strong> <span style="color: #6c757d;">({type_label})</span>')
    client_display.short_description = 'Client'
    
    def montant_display(self, obj):
        return format_html(f'<span style="color: #28a745; font-weight: bold; font-size: 14px;">{obj.montant} FCFA</span>')
    montant_display.short_description = 'Montant'
    
    def mode_paiement_display(self, obj):
        if obj.mode_paiement:
            return format_html(f'<span style="color: #417690;">{obj.mode_paiement.nom}</span>')
        return '-'
    mode_paiement_display.short_description = 'Mode Paiement'
    
    def statut_display(self, obj):
        colors = {'payee': '#28a745', 'en_attente': '#ffc107'}
        color = colors.get(obj.statut, '#6c757d')
        label = obj.get_statut_display()
        return format_html(f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{label}</span>')
    statut_display.short_description = 'Statut'
    
    def montant_total_display(self, obj):
        return format_html(f'<span style="font-weight: bold; font-size: 16px; color: #28a745;">{obj.montant} FCFA</span>')
    montant_total_display.short_description = 'Total'


class LigneCommandeInline(admin.TabularInline):
    """Affichage inline des articles d'une commande"""
    model = LigneCommande
    extra = 1
    fields = ['produit', 'quantite', 'prix_unitaire', 'sous_total']
    readonly_fields = ['sous_total']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('produit')


@admin.register(BonCommande)
class BonCommandeAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date', 'fournisseur_display', 'montant_display', 'livraison_prevue', 'statut_display']
    list_filter = ['statut', 'date', 'fournisseur']
    search_fields = ['numero', 'fournisseur__nom']
    date_hierarchy = 'date'
    readonly_fields = ['date', 'numero', 'montant']
    inlines = [LigneCommandeInline]
    fieldsets = (
        ('Informations Commande', {
            'fields': ('numero', 'date', 'fournisseur')
        }),
        ('Détails', {
            'fields': ('montant', 'livraison_prevue', 'statut')
        }),
    )
    
    def fournisseur_display(self, obj):
        return format_html(f'<strong>{obj.fournisseur.nom}</strong> <span style="color: #6c757d;">({obj.fournisseur.specialite})</span>')
    fournisseur_display.short_description = 'Fournisseur'
    
    def montant_display(self, obj):
        return format_html(f'<span style="color: #28a745; font-weight: bold;">{obj.montant} FCFA</span>')
    montant_display.short_description = 'Montant'
    
    def statut_display(self, obj):
        colors = {'en_cours': '#ffc107', 'livree': '#28a745'}
        color = colors.get(obj.statut, '#6c757d')
        label = obj.get_statut_display()
        return format_html(f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{label}</span>')
    statut_display.short_description = 'Statut'


@admin.register(LigneFacture)
class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ['facture_numero', 'produit_display', 'quantite_display', 'prix_unitaire_display', 'sous_total_display']
    list_filter = ['facture__date', 'produit__categorie']
    search_fields = ['facture__numero', 'produit__nom']
    readonly_fields = ['facture', 'produit', 'quantite', 'prix_unitaire', 'sous_total']
    
    def facture_numero(self, obj):
        return format_html(f'<strong>{obj.facture.numero}</strong>')
    facture_numero.short_description = 'Facture'
    
    def produit_display(self, obj):
        return format_html(f'<strong>{obj.produit.nom}</strong> <span style="color: #6c757d;">({obj.produit.code})</span>')
    produit_display.short_description = 'Produit'
    
    def quantite_display(self, obj):
        return format_html(f'<span style="color: #417690; font-weight: bold;">{obj.quantite}</span>')
    quantite_display.short_description = 'Quantité'
    
    def prix_unitaire_display(self, obj):
        return format_html(f'<span style="color: #28a745;">{obj.prix_unitaire} FCFA</span>')
    prix_unitaire_display.short_description = 'Prix Unitaire'
    
    def sous_total_display(self, obj):
        return format_html(f'<span style="color: #28a745; font-weight: bold; font-size: 14px;">{obj.sous_total} FCFA</span>')
    sous_total_display.short_description = 'Sous-total'


@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = ['commande_numero', 'produit_display', 'quantite_display', 'prix_unitaire_display', 'sous_total_display']
    list_filter = ['commande__date', 'produit__categorie']
    search_fields = ['commande__numero', 'produit__nom']
    readonly_fields = ['commande', 'produit', 'quantite', 'prix_unitaire', 'sous_total']
    
    def commande_numero(self, obj):
        return format_html(f'<strong>{obj.commande.numero}</strong>')
    commande_numero.short_description = 'Commande'
    
    def produit_display(self, obj):
        return format_html(f'<strong>{obj.produit.nom}</strong> <span style="color: #6c757d;">({obj.produit.code})</span>')
    produit_display.short_description = 'Produit'
    
    def quantite_display(self, obj):
        return format_html(f'<span style="color: #417690; font-weight: bold;">{obj.quantite}</span>')
    quantite_display.short_description = 'Quantité'
    
    def prix_unitaire_display(self, obj):
        return format_html(f'<span style="color: #28a745;">{obj.prix_unitaire} FCFA</span>')
    prix_unitaire_display.short_description = 'Prix Unitaire'
    
    def sous_total_display(self, obj):
        return format_html(f'<span style="color: #28a745; font-weight: bold; font-size: 14px;">{obj.sous_total} FCFA</span>')
    sous_total_display.short_description = 'Sous-total'


# ========== PERSONNALISATION DU SITE ADMIN ===========

admin.site.site_header = "Gestion Quincaillerie - Administration"
admin.site.site_title = "Admin Quincaillerie"
admin.site.index_title = "Tableau de bord administrateur"