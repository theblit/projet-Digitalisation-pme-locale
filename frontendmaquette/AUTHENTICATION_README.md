# 🔐 Système d'Authentification - Quincaillerie

## 📋 Vue d'Ensemble

Un système complet de connexion et d'inscription a été implémenté avant d'accéder à l'application. Les utilisateurs doivent se connecter ou créer un compte pour accéder aux fonctionnalités de gestion.

---

## ✨ Fonctionnalités

### 1. **Page de Connexion** (`/login/`)
- Interface élégante et responsive
- Validation des identifiants
- Messages de bienvenue personnalisés
- Lien vers la page d'inscription

**Identifiants de test :**
- Username: `testuser` | Password: `Test@2025`
- Username: `admin` | Password: `Admin@2025`

### 2. **Page d'Inscription** (`/register/`)
- Formulaire d'enregistrement complet
- Validation des champs:
  - Nom d'utilisateur: minimum 3 caractères, unique
  - Mot de passe: minimum 6 caractères
  - Confirmation du mot de passe
- Messages de validation clairs
- Connexion automatique après inscription

### 3. **Profil Utilisateur** (`/profile/`)
- Affichage des informations personnelles
- Modification du nom complet et email
- Historique de connexion
- Lien vers la déconnexion

### 4. **Système de Messages**
Les utilisateurs reçoivent des messages de statut à chaque action:
- ✅ **Succès**: "Bienvenue [Nom] ! Vous êtes connecté"
- ✅ **Succès**: "Compte créé avec succès ! Bienvenue [Nom]"
- ❌ **Erreur**: "Nom d'utilisateur ou mot de passe incorrect"
- ❌ **Erreur**: Validation des champs d'inscription
- 👋 **Déconnexion**: "Au revoir [Nom] ! Vous avez été déconnecté"

### 5. **Protection des Routes**
Toutes les pages de gestion nécessitent l'authentification:
- Dashboard
- Stocks
- Ventes
- Achats
- Clients
- Rapports

---

## 🗂️ Structure des Fichiers

### Vues (`gestion/views.py`)
```python
def login_view(request)              # Connexion
def register_view(request)           # Inscription
def logout_view(request)             # Déconnexion
def profile_view(request)            # Profil utilisateur
```
Toutes les autres vues protégées par `@login_required(login_url='gestion:login')`

### Templates
- `templates/gestion/login.html`     - Page de connexion
- `templates/gestion/register.html`  - Page d'inscription
- `templates/gestion/profile.html`   - Profil utilisateur
- `templates/gestion/base.html`      - Menu utilisateur intégré

### URLs (`gestion/urls.py`)
```
/login/       → login_view
/register/    → register_view
/logout/      → logout_view
/profile/     → profile_view
/             → dashboard (protégé)
/stocks/      → stocks (protégé)
/ventes/      → ventes (protégé)
/achats/      → achats (protégé)
/clients/     → clients (protégé)
/rapports/    → rapports (protégé)
```

### Configuration (`quincaillerie_project/settings.py`)
```python
LOGIN_URL = 'gestion:login'                    # Page de connexion par défaut
LOGIN_REDIRECT_URL = 'gestion:dashboard'       # Redirection après connexion
LOGOUT_REDIRECT_URL = 'gestion:login'          # Redirection après déconnexion

MESSAGE_TAGS = {
    messages.SUCCESS: 'success',
    messages.ERROR: 'error',
    messages.WARNING: 'warning',
    messages.INFO: 'info',
}
```

---

## 🎨 Interface Utilisateur

### Barre Latérale (Sidebar)
- Affichage du nom de l'utilisateur connecté
- Bouton "Mon Profil"
- Bouton "Déconnexion"

### Alertes de Messages
- Affichées en haut du contenu principal
- Codage couleur: erreur (rouge), succès (vert), info (bleu)
- Peut être fermées manuellement
- Animation de glissement automatique

### Styles CSS
- Dégradé violet pour la page de connexion
- Animations fluides
- Design responsive mobile-friendly
- Dark/Light mode compatible

---

## 🚀 Utilisation

### Créer un Nouveau Compte
1. Accédez à `http://127.0.0.1:8000/register/`
2. Remplissez le formulaire (minimum 3 caractères pour l'username, 6 pour le password)
3. Confirmez le mot de passe
4. Cliquez sur "Créer mon compte"
5. Connexion automatique au dashboard

### Se Connecter
1. Accédez à `http://127.0.0.1:8000/login/`
2. Entrez votre nom d'utilisateur et mot de passe
3. Cliquez sur "Se connecter"
4. Un message de bienvenue apparaît

### Modifier le Profil
1. Cliquez sur "Mon Profil" dans la barre latérale
2. Modifiez votre nom complet ou email
3. Cliquez sur "Enregistrer les modifications"

### Se Déconnecter
1. Cliquez sur "Déconnexion" dans la barre latérale
2. Message de confirmation affiché
3. Redirection vers la page de connexion

---

## 🔒 Sécurité

### Protection
- ✅ Utilisation de `@login_required` sur toutes les vues sensibles
- ✅ Validation des mots de passe via Django
- ✅ Protection CSRF intégrée
- ✅ Hachage sécurisé des mots de passe
- ✅ Sessions utilisateur

### Fonctionnalités Futures
- [ ] Réinitialisation de mot de passe par email
- [ ] Authentification à deux facteurs
- [ ] Contrôle d'accès basé sur les rôles
- [ ] Historique des connexions

---

## 📊 Comptes Fournis

| Username | Password | Rôle |
|----------|----------|------|
| `admin` | `Admin@2025` | Super utilisateur |
| `testuser` | `Test@2025` | Utilisateur test |

---

## ⚙️ Configuration Personnalisée

Vous pouvez créer d'autres utilisateurs via:

### Option 1: Django Admin
```bash
python manage.py createsuperuser
```

### Option 2: Script Python
```bash
python create_test_user.py
```

### Option 3: Interface d'inscription
1. Accédez à `/register/`
2. Créez un nouveau compte directement

---

## 📝 Prochaines Étapes Recommandées

1. **Réinitialisation de mot de passe**: Ajouter une vue pour réinitialiser le mot de passe
2. **Authentification par email**: Vérifier l'email lors de l'inscription
3. **Rôles utilisateurs**: Implémenter des groupes Django pour différents niveaux d'accès
4. **Audit**: Logger les connexions/déconnexions pour la sécurité

---

**Statut**: ✅ Implémenté et Testé
**Dernière mise à jour**: 24 Novembre 2025
