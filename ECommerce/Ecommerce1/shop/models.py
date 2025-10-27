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
    category = models.ForeignKey(Category, related_name= 'categorie', on_delete=models.CASCADE)
    image = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
