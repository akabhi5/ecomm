# Generated by Django 4.2.7 on 2023-11-16 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('product', '0001_initial'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('customer', 'product')},
        ),
    ]
