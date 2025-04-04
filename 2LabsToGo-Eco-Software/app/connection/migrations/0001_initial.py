# Generated by Django 3.2.5 on 2023-10-18 08:54

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
            name='Connection_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oc_lab', models.CharField(max_length=120, verbose_name='Port')),
                ('baudrate', models.DecimalField(decimal_places=0, max_digits=6)),
                ('timeout', models.DecimalField(decimal_places=0, max_digits=4)),
                ('time_of_connection', models.DateTimeField(auto_now_add=True)),
                ('auth_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Monitor_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitortext', models.TextField(blank=True)),
                ('connection', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='connection.connection_db')),
            ],
        ),
    ]
