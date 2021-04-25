# Generated by Django 3.2 on 2021-04-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20210408_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient_id',
            name='pump_picture',
            field=models.ImageField(default='../../img/default.png', height_field=500, upload_to='../../img', width_field=400),
        ),
        migrations.AlterField(
            model_name='menu',
            name='picture',
            field=models.ImageField(default='../../img/cocktail_PNG173.png', upload_to='../../img/'),
        ),
    ]