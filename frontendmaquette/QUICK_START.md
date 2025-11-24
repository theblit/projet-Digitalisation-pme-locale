# 🎯 Guide d'Utilisation - Système d'Authentification

## 🚀 Démarrage Rapide

### 1️⃣ Lancer l'Application
```bash
python manage.py runserver
```
Accédez à: `http://127.0.0.1:8000/`

### 2️⃣ Vous Serez Redirigé vers la Page de Connexion
Automatiquement redirigé car vous n'êtes pas connecté.

---

## 📝 Scénario 1: Se Connecter avec un Compte Existant

### Identifiants Disponibles
```
Username: testuser
Password: Test@2025
```

### Étapes
1. Entrez `testuser` dans le champ "Nom d'utilisateur"
2. Entrez `Test@2025` dans le champ "Mot de passe"
3. Cliquez sur **"Se connecter"**
4. ✅ Message: "Bienvenue Utilisateur ! Vous êtes connecté"
5. 🏠 Redirection vers le **Dashboard**

---

## 📝 Scénario 2: Créer un Nouveau Compte

### Étapes
1. Sur la page de connexion, cliquez sur **"Créer un compte maintenant"**
2. Remplissez le formulaire:
   - **Nom d'utilisateur**: `moncompte` (minimum 3 caractères, unique)
   - **Nom complet**: `Jean Dupont` (optionnel)
   - **Email**: `jean@example.com` (optionnel)
   - **Mot de passe**: `SecurePass123` (minimum 6 caractères)
   - **Confirmer mot de passe**: `SecurePass123` (doit correspondre)

3. Cliquez sur **"Créer mon compte"**
4. ✅ Message: "Compte créé avec succès ! Bienvenue Jean Dupont"
5. 🏠 Connexion automatique au **Dashboard**

### Messages d'Erreur Possibles
- ❌ "Le nom d'utilisateur doit contenir au moins 3 caractères"
- ❌ "Ce nom d'utilisateur existe déjà"
- ❌ "Cet email est déjà utilisé"
- ❌ "Le mot de passe doit contenir au moins 6 caractères"
- ❌ "Les mots de passe ne correspondent pas"

---

## 👤 Scénario 3: Modifier Mon Profil

### Étapes
1. Une fois connecté, cliquez sur le menu utilisateur en bas de la **barre latérale**
2. Cliquez sur **"Mon Profil"**
3. Modifiez:
   - Nom complet
   - Adresse email
4. Cliquez sur **"💾 Enregistrer les modifications"**
5. ✅ Message: "Profil mis à jour avec succès"

### Champs Non Modifiables
- **Nom d'utilisateur**: Immuable pour la sécurité
- **Date d'inscription**: Historique
- **Dernière connexion**: Historique

---

## 🚪 Scénario 4: Se Déconnecter

### Étapes
1. En bas de la **barre latérale**, cliquez sur le bouton **"Déconnexion"**
2. ✅ Message: "Au revoir [Votre Nom] ! Vous avez été déconnecté"
3. 🔐 Redirection vers la **page de connexion**

---

## 🎯 Après la Connexion: Fonctionnalités Disponibles

Une fois connecté, vous accédez à:

| Page | URL | Description |
|------|-----|-------------|
| 📊 Tableau de Bord | `/` | Vue d'ensemble et statistiques |
| 📦 Gestion des Stocks | `/stocks/` | Gérer l'inventaire des produits |
| 💰 Ventes | `/ventes/` | Gérer les factures et ventes |
| 🛒 Achats | `/achats/` | Gérer les commandes fournisseurs |
| 👥 Clients | `/clients/` | Gérer la base clients |
| 📈 Rapports | `/rapports/` | Analyser les données |
| 👤 Mon Profil | `/profile/` | Modifier vos infos personnelles |

---

## 🔍 Remarques Importantes

### ✅ Ce Qui Fonctionne
- ✅ Connexion sécurisée
- ✅ Création de compte avec validation
- ✅ Messages personnalisés à chaque action
- ✅ Protection des pages avec authentification
- ✅ Redirection automatique vers connexion si non authentifié
- ✅ Modification du profil utilisateur
- ✅ Déconnexion avec message

### 📧 Notifications par Message
Les messages apparaissent en haut de chaque page:
- 🟢 **Vert** = Succès (inscription, connexion)
- 🔴 **Rouge** = Erreur (mauvais identifiants)
- 🔵 **Bleu** = Info (modifications)
- 🟡 **Jaune** = Avertissement

### 🔒 Sécurité
- Tous les mots de passe sont hachés
- Protection CSRF intégrée
- Sessions sécurisées
- Les données sensibles ne sont jamais affichées

---

## 🐛 Dépannage

### Problème: "Nom d'utilisateur ou mot de passe incorrect"
**Solution**: Vérifiez votre saisie (majuscules/minuscules)

### Problème: "Ce nom d'utilisateur existe déjà"
**Solution**: Choisissez un autre nom d'utilisateur

### Problème: Impossible de créer un compte
**Solution**: Vérifiez les validations:
- Username: minimum 3 caractères, unique
- Password: minimum 6 caractères, doit correspondre

### Problème: Page blanche après connexion
**Solution**: Vérifiez que le serveur est en cours d'exécution:
```bash
python manage.py runserver
```

---

## 📚 Commandes Utiles

### Créer un superutilisateur (admin)
```bash
python manage.py createsuperuser
```

### Créer un utilisateur de test
```bash
python create_test_user.py
```

### Accéder à la console Django
```bash
python manage.py shell
```

### Vider la base de données
```bash
python manage.py flush
```

---

## 📋 Fichiers Modifiés/Créés

### ✨ Nouveaux Fichiers
- `templates/gestion/login.html` - Page de connexion
- `templates/gestion/register.html` - Page d'inscription
- `templates/gestion/profile.html` - Profil utilisateur
- `create_test_user.py` - Script création utilisateur
- `AUTHENTICATION_README.md` - Documentation complète
- `QUICK_START.md` - Ce guide

### 🔧 Fichiers Modifiés
- `gestion/views.py` - Ajout vues auth (login, register, logout, profile)
- `gestion/urls.py` - Ajout routes d'authentification
- `quincaillerie_project/settings.py` - Configuration auth et messages
- `templates/gestion/base.html` - Menu utilisateur + alertes
- `static/css/styles.css` - Styles pour alertes et boutons

---

## ✅ Checklist d'Installation

- [x] Vues d'authentification créées
- [x] Templates HTML créés
- [x] Routes URL configurées
- [x] Décorateurs @login_required appliqués
- [x] Messages système implémentés
- [x] Styles CSS ajoutés
- [x] Utilisateurs de test créés
- [x] Serveur testé et fonctionnel
- [x] Documentation complète

---

**🎉 Votre système d'authentification est prêt à l'emploi!**

Pour toute question ou problème, consultez `AUTHENTICATION_README.md` pour plus de détails.
