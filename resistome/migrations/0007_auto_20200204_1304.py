# Generated by Django 3.0.2 on 2020-02-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resistome', '0006_scaffold_jbrowse_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scaffold',
            name='depth',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Copy #'),
        ),
    ]
