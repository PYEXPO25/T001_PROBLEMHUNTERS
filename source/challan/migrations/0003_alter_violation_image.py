# Generated by Django 5.0.6 on 2025-02-21 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challan', '0002_alter_violation_violation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violation',
            name='image',
            field=models.CharField(default='No image', max_length=300),
            preserve_default=False,
        ),
    ]
