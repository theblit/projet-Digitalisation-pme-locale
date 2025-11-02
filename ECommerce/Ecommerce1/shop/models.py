from django.db import models

# Create your models here.

# pour creer la table categorie
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name


# pour creer la table produit et une relation entre les produits et les categories
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE)
    image = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    

# pour creer la table commande
class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente de paiement'),
        ('paye', 'Payée'),
        ('en_cours', 'En cours de livraison'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    
    PAIEMENT_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('carte', 'Carte bancaire'),
        ('paypal', 'PayPal'),
        ('especes', 'Espèces à la livraison'),
    ]
    
    items = models.TextField()
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    adress = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300, blank=True, null=True)
    telephone = models.CharField(max_length=20)
    
    # Nouveaux champs
    sous_total = models.FloatField(default=0)
    frais_livraison = models.FloatField(default=0)
    code_promo = models.CharField(max_length=50, blank=True, null=True)
    reduction = models.FloatField(default=0)
    total = models.FloatField(default=0)
    
    methode_paiement = models.CharField(max_length=50, choices=PAIEMENT_CHOICES, default='mobile_money')
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    
    date_commande = models.DateTimeField(auto_now_add=True)
    date_paiement = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date_commande']

    def __str__(self):
        return f"Commande #{self.id} - {self.nom}"
    

# pour creer la table code promo
class CodePromo(models.Model):   
    code = models.CharField(max_length=50, unique=True)
    reduction_pourcentage = models.FloatField(default=0)  # Réduction en %
    reduction_montant = models.FloatField(default=0)  # Réduction en montant fixe
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    actif = models.BooleanField(default=True)
    utilisations_max = models.IntegerField(default=100)
    utilisations_actuelles = models.IntegerField(default=0)
    
    def __str__(self):
        return self.code
    
    def est_valide(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.actif and
            self.date_debut <= now <= self.date_fin and
            self.utilisations_actuelles < self.utilisations_max
        ) 