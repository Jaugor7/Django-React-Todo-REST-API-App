# Generated by Django 3.1.3 on 2020-11-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Discourse_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Posts',
        ),
    ]