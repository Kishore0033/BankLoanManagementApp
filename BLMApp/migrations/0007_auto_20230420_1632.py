# Generated by Django 3.2.3 on 2023-04-20 11:02

import BLMApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BLMApp', '0006_auto_20230420_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyloan',
            name='kyc_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='applyloan',
            name='loan_id',
            field=models.CharField(default='YB2023041632', editable=False, max_length=40),
        ),
        migrations.AlterField(
            model_name='kycregistration',
            name='kyc_id',
            field=models.IntegerField(default=BLMApp.models.generate_unique_id, editable=False, unique=True),
        ),
    ]
