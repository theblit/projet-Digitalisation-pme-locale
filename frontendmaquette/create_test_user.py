#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quincaillerie_project.settings')
django.setup()

from django.contrib.auth.models import User

# Créer utilisateur de test
User.objects.filter(username='testuser').delete()
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='Test@2025',
    first_name='Utilisateur'
)
print(f"✓ Utilisateur créé: {user.username} ({user.first_name})")

# Vérifier les utilisateurs
users = User.objects.all()
print(f"\nUtilisateurs dans la base de données:")
for u in users:
    print(f"  - {u.username} ({u.first_name or 'Sans nom'})")
