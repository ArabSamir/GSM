# Generated by Django 3.1.6 on 2021-02-08 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Achat', '0008_delete_couleur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vente',
            name='num_vente',
        ),
    ]
