# Generated manually for longer formatted phone numbers (e.g. +63 …).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turo_api', '0017_profilecredentialdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
