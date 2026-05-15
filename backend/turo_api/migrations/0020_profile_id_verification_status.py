from django.db import migrations, models


def backfill_verification_status(apps, schema_editor):
    Profile = apps.get_model('turo_api', 'Profile')
    # Existing users who already had requires_id_verification=False are already verified
    Profile.objects.filter(requires_id_verification=False).update(id_verification_status='approved')

class Migration(migrations.Migration):

    dependencies = [
        ('turo_api', '0019_profile_id_photo_profile_requires_id_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_verification_status',
            field=models.CharField(choices=[('not_submitted', 'Not Submitted'), ('pending', 'Pending Admin Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='not_submitted', max_length=20),
        ),
        migrations.RunPython(backfill_verification_status),
    ]
