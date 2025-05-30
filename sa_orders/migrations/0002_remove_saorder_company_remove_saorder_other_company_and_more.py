# Generated by Django 4.2.21 on 2025-05-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sa_orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="saorder",
            name="company",
        ),
        migrations.RemoveField(
            model_name="saorder",
            name="other_company",
        ),
        migrations.AddField(
            model_name="saorder",
            name="companies",
            field=models.JSONField(
                default=list,
                help_text="List of selected company keys (e.g. ['adendorff', 'chemvulc'])",
            ),
        ),
        migrations.AlterField(
            model_name="saorder",
            name="client_rate",
            field=models.FloatField(
                help_text="The conversion rate given to the client"
            ),
        ),
        migrations.AlterField(
            model_name="saorder",
            name="delivery_cost",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Cost for delivery to client in Zim in USD",
                max_digits=10,
            ),
        ),
        migrations.AlterField(
            model_name="saorder",
            name="my_zar_rate",
            field=models.FloatField(help_text="The ZAR rate for USD conversion"),
        ),
        migrations.AlterField(
            model_name="saorder",
            name="pick_up_cost",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Cost for picking from companies in ZAR",
                max_digits=10,
            ),
        ),
        migrations.AlterField(
            model_name="saorder",
            name="transport_cost",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Cost for transporting to Zim in ZAR",
                max_digits=10,
            ),
        ),
        migrations.AlterField(
            model_name="saorder",
            name="zar_amount",
            field=models.DecimalField(
                decimal_places=2, help_text="The total order cost in ZAR", max_digits=10
            ),
        ),
    ]
