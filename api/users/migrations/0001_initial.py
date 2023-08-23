# Generated by Django 4.2.4 on 2023-08-21 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('first_name', models.TextField(db_column='FirstName', default='')),
                ('last_name', models.TextField(db_column='LastName', default='')),
                ('approved_by_user', models.IntegerField(db_column='ApprovedByUser', default=0)),
                ('is_active', models.BooleanField(db_column='IsActive', default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('is_approved', models.BooleanField(db_column='IsApproved', default=False, help_text='Designates whether this user is approved or not.')),
                ('email', models.EmailField(db_column='Email', help_text='Email Field', max_length=254, null=True, unique=True)),
                ('is_email_verified', models.BooleanField(db_column='IsEmailVerified', default=False)),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.')),
                ('is_deleted', models.BooleanField(db_column='IsDeleted', default=False)),
                ('fcm', models.TextField(db_column='FCM', default=None, null=True)),
                ('date_of_birth', models.DateField(db_column='DateOfBirth', null=True)),
                ('gender', models.CharField(db_column='Gender', max_length=255, null=True)),
                ('phone', models.CharField(db_column='Phone', max_length=255, null=True)),
                ('city', models.CharField(db_column='City', max_length=255, null=True)),
                ('cnic', models.CharField(db_column='Cnic', max_length=255, null=True)),
                ('ibn', models.CharField(db_column='BankAccount', max_length=255, null=True)),
                ('ntn', models.CharField(db_column='NTN', max_length=255, null=True)),
                ('google_id', models.CharField(max_length=255, null=True, unique=True)),
                ('facebook_id', models.CharField(max_length=255, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'db_table': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('name', models.CharField(db_column='Name', max_length=255, unique=True)),
                ('code', models.SlugField(db_column='Code', default='')),
                ('description', models.TextField(blank=True, db_column='Description', null=True)),
                ('access_level', models.IntegerField(choices=[(500, 'Customer'), (900, 'Super Admin')], db_column='AccessLevel', default=500)),
            ],
            options={
                'db_table': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='EmailVerificationLink',
            fields=[
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('token', models.CharField(db_column='Token', max_length=255, primary_key=True, serialize=False, unique=True)),
                ('code', models.IntegerField(blank=True, db_column='Code', default=None, null=True)),
                ('expiry_at', models.DateTimeField(db_column='ExpireAt')),
                ('user', models.ForeignKey(db_column='UserId', on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Trainee_Email_Verification',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, db_column='RoleId', default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to='users.role'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]