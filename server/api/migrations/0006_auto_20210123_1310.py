# Generated by Django 3.1.5 on 2021-01-23 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210123_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratio',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]