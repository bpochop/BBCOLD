# Generated by Django 3.2 on 2021-04-13 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_delete_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_progress', models.CharField(max_length=1)),
            ],
        ),
    ]