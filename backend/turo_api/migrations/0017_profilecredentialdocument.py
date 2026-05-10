from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turo_api', '0016_remove_profile_achievement_proof_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileCredentialDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='tutor_credentials/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credential_documents', to='turo_api.profile')),
            ],
            options={
                'ordering': ['-uploaded_at', '-id'],
            },
        ),
    ]
