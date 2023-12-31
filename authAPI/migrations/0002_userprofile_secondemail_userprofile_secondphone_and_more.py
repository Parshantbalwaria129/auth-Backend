# Generated by Django 4.2.3 on 2023-10-24 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='secondEmail',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='secondPhone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='phoneotpmodel',
            name='phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
