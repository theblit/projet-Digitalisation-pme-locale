from django.db import migrations
from django.db.models import Sum

def update_client_totals(apps, schema_editor):
    """Mettre à jour les totaux d'achats des clients basés sur les factures existantes"""
    Client = apps.get_model('gestion', 'Client')
    Facture = apps.get_model('gestion', 'Facture')
    
    for client in Client.objects.all():
        total = Facture.objects.filter(client=client).aggregate(total=Sum('montant'))['total'] or 0
        client.total_achats = total
        client.save()

def reverse_func(apps, schema_editor):
    """Fonction inverse - réinitialiser les totaux à 0"""
    Client = apps.get_model('gestion', 'Client')
    Client.objects.all().update(total_achats=0)

class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_lignefacture'),
    ]

    operations = [
        migrations.RunPython(update_client_totals, reverse_func),
    ]
