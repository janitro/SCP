# Generated by Django 3.1.2 on 2020-10-20 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('is_admin', models.BooleanField(default=False, null=True)),
                ('is_prof', models.BooleanField(default=False, null=True)),
                ('is_cliente', models.BooleanField(default=False, null=True)),
            ],
            options={
                'db_table': 'login',
                'managed': False,
            },
        ),
    ]
