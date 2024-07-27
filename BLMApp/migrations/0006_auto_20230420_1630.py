# Generated by Django 3.2.3 on 2023-04-20 11:00

import BLMApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BLMApp', '0005_auto_20230418_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyloan',
            name='approval_status',
            field=models.CharField(choices=[('Approved', 'Approve'), ('Rejected', 'Reject')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='applyloan',
            name='loan_id',
            field=models.CharField(default='YB2023041630', editable=False, max_length=40),
        ),
        migrations.AlterField(
            model_name='kycregistration',
            name='kyc_id',
            field=models.IntegerField(default=BLMApp.models.generate_unique_id, editable=False),
        ),
        migrations.AlterField(
            model_name='kycregistration',
            name='kyc_status',
            field=models.CharField(choices=[('Approved', 'Approve'), ('Rejected', 'Reject')], default='Pending', max_length=20),
        ),
    ]
