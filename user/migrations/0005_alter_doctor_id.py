# Generated by Django 5.1.6 on 2025-02-28 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_doctor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='id',
            field=models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
    ]
