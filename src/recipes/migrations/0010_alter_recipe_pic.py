# Generated by Django 5.0.1 on 2024-02-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_recipe_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='pic',
            field=models.ImageField(default='img/default.jpg', upload_to='recipe_pics'),
        ),
    ]