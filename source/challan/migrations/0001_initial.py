# Generated by Django 5.0.6 on 2025-02-21 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_plate', models.CharField(max_length=20)),
                ('violation_time', models.DateTimeField(auto_now_add=True)),
                ('fine_amount', models.IntegerField(default=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='violations/')),
            ],
        ),
    ]
