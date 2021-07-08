# Generated by Django 2.2 on 2021-07-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('reg_number', models.CharField(blank=True, max_length=100, null=True)),
                ('established_date', models.DateField(blank=True, null=True)),
                ('details', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
