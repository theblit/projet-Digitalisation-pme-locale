#!/bin/bash
# Script de démarrage - Système d'Authentification Quincaillerie

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  🔐 Système d'Authentification - Quincaillerie Management System  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier l'environnement virtuel
if [ ! -d "env" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "📦 Installation de l'environnement virtuel..."
    python -m venv env
    echo "✅ Environnement créé"
fi

# Activer l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source env/Scripts/activate 2>/dev/null || . env/Scripts/activate

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
pip install -q -r requirements.txt 2>/dev/null || echo "ℹ️  Pas de requirements.txt"

# Migrations
echo "🗄️  Application des migrations..."
python manage.py migrate --noinput

# Créer un utilisateur de test si nécessaire
echo "👤 Création d'utilisateurs de test..."
python create_test_user.py

# Afficher les infos
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                      INFORMATIONS DE DÉMARRAGE                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ Configuration Complète"
echo ""
echo "📍 Accès à l'Application:"
echo "   🌐 http://127.0.0.1:8000/"
echo "   🔐 http://127.0.0.1:8000/login/"
echo ""
echo "👤 Utilisateurs de Test:"
echo "   • Username: testuser   | Password: Test@2025"
echo "   • Username: admin      | Password: Admin@2025"
echo ""
echo "📚 Documentation:"
echo "   • QUICK_START.md               - Guide de démarrage rapide"
echo "   • AUTHENTICATION_README.md     - Documentation complète"
echo "   • TEST_CASES.md                - Cas de test détaillés"
echo "   • DOCUMENTATION_INDEX.md       - Index de la documentation"
echo ""
echo "🚀 Pour Démarrer:"
echo "   python manage.py runserver"
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo ""
