from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_datetime
from django.views import generic
from rest_framework import viewsets

from decimal import Decimal
from . import coin_api
from .models import Coin, CoinList, Transaction
from .serializers import CoinListSerializer


def index(request):
    return render(request, 'index.html')


class HomeView(LoginRequiredMixin, generic.ListView):
    model = Coin
    template_name = 'home.html'

    def get_queryset(self):
        coins = Coin.objects.filter(user=self.request.user).order_by('-total_cost')
        coin_api.fetch_prices(coins)
        return coins


@login_required
def detail(request, coin_ticker):
    coin = get_object_or_404(Coin, coin_ticker=coin_ticker, user=request.user)
    recent_transactions = coin.transaction_set.filter(parsed=True).order_by('-transaction_date')[:10]
    image_url = None

    return render(request, 'detail.html', {
        'coin': coin,
        'transactions': recent_transactions,
        'image_url': image_url,
    })


# https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-editing/
class RegisterView(SuccessMessageMixin, generic.edit.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('AppCoinStash:home')
    template_name = 'registration/register.html'
    success_message = "Registered successfully!"


class CoinSearchViewSet(viewsets.ModelViewSet):
    serializer_class = CoinListSerializer

    def get_queryset(self):
        search_string = self.request.query_params.get('search_string')
        queryset = CoinList.objects.filter(
            Q(coin_symbol__iexact=search_string) | Q(coin_name__istartswith=search_string))\
            .order_by('coin_name')
        return queryset[:10]


@login_required
def add_coin(request):
    coin_id = request.POST.get('new_coin')
    coin_data = CoinList.objects.filter(coin_id=coin_id)
    if not coin_data:
        messages.error(request, 'The coin is currently not supported.')
    else:
        cdata = coin_data[0]
        if Coin.objects.filter(user=request.user, coin_ticker=cdata.coin_symbol).exists():
            messages.error(request, 'The coin is already in your portfolio.')
        else:
            new_coin = Coin(user=request.user,
                            coin_ticker=cdata.coin_symbol,
                            coin_name=cdata.coin_name,
                            coin_api_id=cdata.coin_id)
            new_coin.save()
            messages.success(request, 'Coin added successfully.')
    return redirect('home/')


@login_required
def add_transaction(request):
    coin = Coin.objects.get(user=request.user, coin_ticker=request.POST.get('coin_ticker'))
    if coin:
        trans_type = int(request.POST.get('trans_type'))
        datetime = parse_datetime(request.POST.get('datetime'))
        sent_qty = Decimal(request.POST.get('sent_qty'))
        recv_qty = Decimal(request.POST.get('recv_qty'))
        transaction = Transaction(coin=coin,
                                  transaction_type=trans_type,
                                  transaction_date=datetime,
                                  received_qty=recv_qty,
                                  sent_qty=sent_qty,
                                  parsed=False)
        transaction.save()
        coin.parse_transaction(transaction=transaction)
        messages.success(request, 'Added transaction successfully.')
    else:
        messages.error(request, 'Coin not found.')

    return redirect('AppCoinStash:detail', coin_ticker=request.POST.get('coin_ticker'))


@login_required
def del_transaction(request):
    transaction = Transaction.objects.get(id=request.POST.get('tx_id'))
    coin = Coin.objects.get(coin_ticker=request.POST.get('coin_ticker'))
    if transaction and coin:
        transaction.delete()
        coin.reparse_transaction_history()
    else:
        messages.error(request, 'Could not delete transaction.')

    return redirect('AppCoinStash:detail', coin_ticker=request.POST.get('coin_ticker'))


@login_required
def del_coin(request):
    coin = Coin.objects.get(user=request.user, coin_ticker=request.POST.get('coin_ticker'))
    if coin:
        coin.delete()
        messages.warning(request, request.POST.get('coin_ticker').capitalize() + ' removed from portfolio.')
    else:
        messages.error(request, 'Could not remove coin.')
    return redirect('AppCoinStash:home')
    pass


@login_required
def get_chart_data(request):
    coins = Coin.objects.filter(user=request.user).order_by('-total_cost')
    rsp = {}
    for coin in coins:
        if coin.total_cost > 0:
            rsp.__setitem__(coin.coin_ticker.upper(), coin.total_cost)
    return JsonResponse(rsp)
