# Generated by Django 3.2.7 on 2021-10-14 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('contrasena', models.CharField(max_length=100)),
            ],
        ),
    ]
