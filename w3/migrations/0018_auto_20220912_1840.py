# Generated by Django 3.2.9 on 2022-09-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w3', '0017_auto_20220608_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountmetamask',
            name='private_key',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='data',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
