# Generated by Django 3.2.3 on 2021-06-02 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_alter_ratio_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratio',
            name='amount',
            field=models.CharField(max_length=4),
        ),
    ]
