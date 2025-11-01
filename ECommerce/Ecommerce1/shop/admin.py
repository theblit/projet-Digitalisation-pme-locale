from django.contrib import admin
from .models import Category, Product, Commande

# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display = ('name','date_added')
    search_fields = ('name',)


class AdminProduct(admin.ModelAdmin):
    list_display = ('title','price','category','date_added')
    search_fields = ('title','category__name')


class AdminCommande(admin.ModelAdmin):
    list_display = ('id', 'nom', 'email', 'adress', 'ville', 'pays','total',  'date_commande')  # CORRIGÉ: adress au lieu de address
    search_fields = ('nom', 'email')
    list_filter = ('pays', 'ville', 'date_commande')
    readonly_fields = ('date_commande',)


admin.site.register(Category, AdminCategory)
admin.site.register(Product, AdminProduct)
admin.site.register(Commande, AdminCommande)