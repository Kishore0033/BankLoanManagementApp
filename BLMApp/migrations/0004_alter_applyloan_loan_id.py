# Generated by Django 3.2.3 on 2023-04-16 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BLMApp', '0003_auto_20230415_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyloan',
            name='loan_id',
            field=models.CharField(default='YB2023041601', editable=False, max_length=40),
        ),
    ]
