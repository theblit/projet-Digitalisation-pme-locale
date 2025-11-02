from django.contrib import admin
from .models import Category, Product, Commande, CodePromo

# Register your models here.
admin.site.site_header = "Ecommerce Administration"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome CEO"



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


class AdminCodePromo(admin.ModelAdmin):
    list_display = ('code', 'reduction_pourcentage', 'reduction_montant', 'actif', 'utilisations_actuelles', 'utilisations_max')
    search_fields = ('code',)
    list_filter = ('actif',)


admin.site.register(Category, AdminCategory)
admin.site.register(Product, AdminProduct)
admin.site.register(Commande, AdminCommande)
admin.site.register(CodePromo, AdminCodePromo)
