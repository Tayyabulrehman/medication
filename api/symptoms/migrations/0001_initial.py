# Generated by Django 4.2.4 on 2023-08-22 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Symptoms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('description', models.TextField(db_column='Description', null=True)),
                ('severity', models.CharField(db_column='Severity', max_length=255, null=True)),
                ('time', models.DateTimeField(null=True)),
                ('duration', models.IntegerField(null=True)),
                ('associated_factors', models.TextField(null=True)),
                ('medications_taken', models.TextField(null=True)),
                ('notes', models.TextField(null=True)),
                ('triggers', models.TextField(null=True)),
                ('user', models.ForeignKey(db_column='UserId', on_delete=django.db.models.deletion.CASCADE, related_name='user_symptoms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Symptoms',
            },
        ),
    ]
