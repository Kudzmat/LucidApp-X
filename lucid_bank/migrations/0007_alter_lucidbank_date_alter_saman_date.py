# Generated by Django 4.2.21 on 2025-05-20 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lucid_bank", "0006_alter_lucidbank_date_alter_saman_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lucidbank",
            name="date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="saman",
            name="date",
            field=models.DateTimeField(),
        ),
    ]
