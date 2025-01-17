# Generated by Django 3.2.3 on 2023-04-15 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BLMApp', '0002_applyloan_loan_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyloan',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='applyloan',
            name='loan_id',
            field=models.CharField(default='YB2023041522:17:46', editable=False, max_length=40),
        ),
    ]
