# Generated by Django 2.0.2 on 2019-10-10 06:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$')], verbose_name='Device MAC Address')),
                ('hostname', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Device hostname')),
                ('last_ip_address', models.CharField(max_length=50, verbose_name='Last check-in IP address')),
                ('owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RunRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='run_request',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='zezere.RunRequest'),
        ),
    ]
