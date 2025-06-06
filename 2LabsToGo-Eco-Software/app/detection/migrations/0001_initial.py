# Generated by Django 3.2.5 on 2025-04-09 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finecontrol', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraControls_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_exposure', models.CharField(choices=[('0', 'off'), ('1', 'on')], default=('0', 'off'), max_length=255, null=True)),
                ('exposure_time_absolute', models.DecimalField(decimal_places=4, default=0.025, max_digits=7, null=True)),
                ('white_balance_auto_preset', models.CharField(choices=[('0', 'off'), ('1', 'auto'), ('2', 'tungsten'), ('3', 'fluorescent'), ('4', 'indoor'), ('5', 'daylight'), ('6', 'cloudy'), ('7', 'custom')], default=('0', 'off'), max_length=255, null=True)),
                ('analogue_gain', models.DecimalField(decimal_places=1, default=None, max_digits=3, null=True)),
                ('colour_gains', models.CharField(default='1.0,1.0', max_length=10, null=True)),
                ('imagenumber', models.DecimalField(decimal_places=0, default=1, max_digits=3, null=True)),
                ('delaytime', models.DecimalField(decimal_places=0, default=0, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=100, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('note', models.TextField(blank=True, default='', null=True)),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leds_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uv365_power', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('uv255_power', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('whitet_power', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('red', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('blue', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('green', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('white', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlatePhoto_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.FileField(upload_to='media/')),
            ],
        ),
        migrations.CreateModel(
            name='UserControls_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brightness', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=2, null=True)),
                ('contrast', models.DecimalField(blank=True, decimal_places=1, default=1, max_digits=3, null=True)),
                ('saturation', models.DecimalField(blank=True, decimal_places=1, default=1, max_digits=3, null=True)),
                ('sharpness', models.DecimalField(blank=True, decimal_places=1, default=1, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hdr_Image',
            fields=[
                ('images_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='detection.images')),
                ('image', models.ImageField(blank=True, default='/default.jpeg', null=True, upload_to='hdr/')),
            ],
            bases=('detection.images',),
        ),
        migrations.CreateModel(
            name='Detection_ZeroPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zero_x', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('zero_y', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Images_Db',
            fields=[
                ('images_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='detection.images')),
                ('image', models.ImageField(default='/default.jpg', upload_to='images/')),
                ('camera_conf', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='detection.cameracontrols_db')),
                ('leds_conf', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='detection.leds_db')),
                ('method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finecontrol.method_db')),
                ('user_conf', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='detection.usercontrols_db')),
            ],
            bases=('detection.images',),
        ),
    ]
