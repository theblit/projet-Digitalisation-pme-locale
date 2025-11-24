@echo off
REM Script de démarrage - Système d'Authentification Quincaillerie (Windows)

cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║  🔐 Système d'Authentification - Quincaillerie Management System  ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Vérifier l'environnement virtuel
if not exist "env" (
    echo ❌ Environnement virtuel non trouvé
    echo 📦 Installation de l'environnement virtuel...
    python -m venv env
    echo ✅ Environnement créé
)

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call env\Scripts\activate.bat

REM Vérifier les dépendances
echo 📦 Vérification des dépendances...
pip install -q django python-dotenv 2>nul || echo ℹ️  Django et dépendances installés

REM Migrations
echo 🗄️  Application des migrations...
python manage.py migrate --noinput

REM Créer un utilisateur de test si nécessaire
echo 👤 Création d'utilisateurs de test...
python create_test_user.py

REM Afficher les infos
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                      INFORMATIONS DE DÉMARRAGE                     ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo ✅ Configuration Complète
echo.
echo 📍 Accès à l'Application:
echo    🌐 http://127.0.0.1:8000/
echo    🔐 http://127.0.0.1:8000/login/
echo.
echo 👤 Utilisateurs de Test:
echo    • Username: testuser   ^| Password: Test@2025
echo    • Username: admin      ^| Password: Admin@2025
echo.
echo 📚 Documentation:
echo    • QUICK_START.md               - Guide de démarrage rapide
echo    • AUTHENTICATION_README.md     - Documentation complète
echo    • TEST_CASES.md                - Cas de test détaillés
echo    • DOCUMENTATION_INDEX.md       - Index de la documentation
echo.
echo 🚀 Pour Démarrer le Serveur:
echo    python manage.py runserver
echo.
echo 💡 Astuce: Appuyez sur Ctrl+C pour arrêter le serveur
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo.

pause
