# Generated by Django 4.2.7 on 2024-03-02 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_productsizequantity_options_and_more'),
        ('cart', '0004_cartitem_size'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product', 'size')},
        ),
    ]
