# Generated by Django 4.2.21 on 2025-05-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sa_orders", "0006_alter_pendingsaorder_date_alter_saorder_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="saorder",
            name="order_delivered",
            field=models.BooleanField(
                default=False, help_text="Has the order been delivered?"
            ),
        ),
        migrations.DeleteModel(
            name="PendingSAOrder",
        ),
    ]
