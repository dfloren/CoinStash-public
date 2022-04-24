from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model

# TODO: React with Parallax frontend
# TODO: Add password reset (Gmail SMTP) and change password
# TODO: Add server-side input validation


class Coin(models.Model):
    COINGECKO = 1
    COINMARKETCAP = 2
    API_TYPE = [
        (COINGECKO, "COINGECKO"),
        (COINMARKETCAP, "COINMARKETCAP"),
    ]

    coin_api_id = models.CharField(max_length=200)
    coin_ticker = models.CharField(max_length=200)
    coin_name = models.CharField(max_length=200)
    coin_api_type = models.PositiveSmallIntegerField(
        choices=API_TYPE,
        default=COINGECKO
    )

    current_price = Decimal(0)
    gain_loss = Decimal(0)
    avg_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    balance = models.DecimalField(max_digits=30, decimal_places=18, default=0.0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.coin_name

    # Must save after calling this function
    def reset_metrics(self):
        self.avg_cost = Decimal(0)
        self.total_cost = Decimal(0)
        self.balance = Decimal(0)

    # Must save after calling this function
    def update_avg_cost(self):
        if self.balance <= 0 or self.total_cost <= 0:  # exited the market
            self.avg_cost = 0
            self.total_cost = 0
        else:
            self.avg_cost = self.total_cost / self.balance

    # Parse a single transaction
    def parse_transaction(self, transaction):
        if transaction.transaction_type == 1:
            self.total_cost += transaction.sent_qty
            self.balance += transaction.received_qty
        else:
            self.total_cost -= self.avg_cost * transaction.sent_qty
            self.balance -= transaction.sent_qty

        self.update_avg_cost()
        transaction.parsed = True
        transaction.save()
        self.save()

    # Parse all transactions
    def reparse_transaction_history(self):
        transactions = Transaction.objects.filter(coin=self).order_by('transaction_date')
        self.reset_metrics()
        self.save()
        for transaction in transactions:
            self.parse_transaction(transaction=transaction)


class Transaction(models.Model):
    """
    Fiat/Coin and Coin/Fiat are the only supported transactions.
    Coin/Coin transactions are not. This enables inference of
    currency of sent and received quantities.
    """
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    BUY = 1
    SELL = 2
    TRANSACTION_TYPE = [
        (BUY, "BUY"),
        (SELL, "SELL"),
    ]

    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE,
        default=BUY
    )
    transaction_date = models.DateTimeField()
    received_qty = models.DecimalField(max_digits=30, decimal_places=18)
    sent_qty = models.DecimalField(max_digits=30, decimal_places=18)
    parsed = models.BooleanField()


class CoinList(models.Model):
    coin_id = models.CharField(max_length=200)
    coin_symbol = models.CharField(max_length=200)
    coin_name = models.CharField(max_length=200)

    def __str__(self):
        return self.coin_name
