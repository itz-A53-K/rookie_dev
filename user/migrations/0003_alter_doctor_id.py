# Generated by Django 5.1.6 on 2025-02-28 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_dob_alter_user_gender_alter_user_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
