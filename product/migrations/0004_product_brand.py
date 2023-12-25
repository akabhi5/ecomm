# Generated by Django 4.2.7 on 2023-12-25 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0002_brand_slug'),
        ('product', '0003_alter_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='brand.brand'),
            preserve_default=False,
        ),
    ]
