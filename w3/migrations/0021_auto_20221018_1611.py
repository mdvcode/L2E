# Generated by Django 3.2.9 on 2022-10-18 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('w3', '0020_auto_20221018_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipfs',
            name='gas',
        ),
        migrations.RemoveField(
            model_name='ipfs',
            name='gas_price',
        ),
        migrations.RemoveField(
            model_name='ipfs',
            name='to_account',
        ),
        migrations.RemoveField(
            model_name='ipfs',
            name='user',
        ),
    ]
