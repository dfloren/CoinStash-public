# Generated by Django 4.0.4 on 2022-04-23 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoinStash', '0003_coin_coin_api_id_alter_coin_avg_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='coin_api_id',
            field=models.CharField(max_length=200),
        ),
    ]
