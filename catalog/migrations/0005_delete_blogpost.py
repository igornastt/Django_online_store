# Generated by Django 4.2.3 on 2023-08-08 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_blogpost'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogPost',
        ),
    ]
