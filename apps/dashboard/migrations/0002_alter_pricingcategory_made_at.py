# Generated by Django 4.0.5 on 2022-07-04 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricingcategory',
            name='made_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
