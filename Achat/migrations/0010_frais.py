# Generated by Django 3.1.6 on 2021-02-17 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Achat', '0009_remove_vente_num_vente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.IntegerField(blank=True, default=0, null=True)),
                ('designation', models.CharField(blank=True, max_length=250, null=True)),
                ('date_sortie', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]