# Generated by Django 3.1.3 on 2020-12-09 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20201128_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotivoVisita',
            fields=[
                ('id_motivo_visita', models.IntegerField(primary_key=True, serialize=False)),
                ('tipo_visita', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'motivo_visita',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='login',
            table='login',
        ),
    ]
