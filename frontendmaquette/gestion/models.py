# gestion/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name_plural = "Catégories"


class ModePaiement(models.Model):
    """Modèle pour les modes de paiement"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name_plural = "Modes de Paiement"


class Produit(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    seuil = models.IntegerField(default=10)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} ({self.code})"
    
    def statut_stock(self):
        if self.stock < self.seuil * 0.5:
            return 'critique'
        elif self.stock < self.seuil:
            return 'faible'
        return 'ok'

class Client(models.Model):
    TYPE_CHOICES = [
        ('particulier', 'Particulier'),
        ('professionnel', 'Professionnel'),
    ]
    nom = models.CharField(max_length=200)
    type_client = models.CharField(max_length=20, choices=TYPE_CHOICES)
    telephone = models.CharField(max_length=20)
    credit_en_cours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_achats = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['-date_creation']

class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    specialite = models.CharField(max_length=200)
    total_commandes_mois = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['-date_creation']

class Facture(models.Model):
    STATUT_CHOICES = [
        ('payee', 'Payée'),
        ('en_attente', 'En attente'),
    ]
    numero = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    
    def __str__(self):
        return f"{self.numero} - {self.client.nom} ({self.montant} FCFA)"

class LigneFacture(models.Model):
    """Article individuel dans une facture"""
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.facture.numero} - {self.produit.nom} x{self.quantite}"
    
    class Meta:
        ordering = ['id']

class BonCommande(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
    ]
    numero = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    livraison_prevue = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    
    def __str__(self):
        return f"{self.numero} - {self.fournisseur.nom} ({self.montant} FCFA)"


class LigneCommande(models.Model):
    """Modèle pour les articles d'une commande"""
    commande = models.ForeignKey(BonCommande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"
    
    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"