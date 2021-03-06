# Generated by Django 4.0.4 on 2022-04-20 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_ticker', models.CharField(max_length=200)),
                ('coin_name', models.CharField(max_length=200)),
                ('coin_api_type', models.PositiveSmallIntegerField(choices=[(1, 'COINGECKO'), (2, 'COINMARKETCAP')], default=1)),
                ('avg_cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('balance', models.DecimalField(decimal_places=18, max_digits=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.PositiveSmallIntegerField(choices=[(1, 'BUY'), (1, 'SELL')], default=1)),
                ('transaction_date', models.DateTimeField()),
                ('transaction_fee', models.DecimalField(decimal_places=18, max_digits=30)),
                ('received_qty', models.DecimalField(decimal_places=18, max_digits=30)),
                ('sent_qty', models.DecimalField(decimal_places=18, max_digits=30)),
                ('parsed', models.BooleanField()),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppCoinStash.coin')),
            ],
        ),
    ]
