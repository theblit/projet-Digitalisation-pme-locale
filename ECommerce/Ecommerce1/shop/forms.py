from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilVendeur, Product, Category

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nom_boutique = forms.CharField(max_length=200, required=True, label="Nom de votre boutique")
    telephone = forms.CharField(max_length=20, required=True, label="Téléphone")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nom_boutique', 'telephone')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Créer le profil vendeur
            ProfilVendeur.objects.create(
                user=user,
                nom_boutique=self.cleaned_data['nom_boutique'],
                telephone=self.cleaned_data['telephone']
            )
        return user


class ProfilVendeurForm(forms.ModelForm):
    class Meta:
        model = ProfilVendeur
        fields = ['nom_boutique', 'description', 'telephone', 'adresse', 'ville', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'category', 'image', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Titre du produit',
            'price': 'Prix (XOF)',
            'description': 'Description',
            'category': 'Catégorie',
            'image': 'URL de l\'image',
            'stock': 'Quantité en stock',
        }