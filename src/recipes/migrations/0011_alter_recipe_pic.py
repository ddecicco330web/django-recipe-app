# Generated by Django 5.0.1 on 2024-02-25 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_recipe_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='pic',
            field=models.ImageField(default='static/img/default.jpg', upload_to='recipe_pics'),
        ),
    ]
