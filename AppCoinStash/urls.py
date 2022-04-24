from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'coinsearch', views.CoinSearchViewSet, basename='coinsearch')

app_name = 'AppCoinStash'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('<str:coin_ticker>/detail', views.detail, name='detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.RegisterView.as_view(), name="register"),
    path('', include(router.urls)),
    path('add_coin', views.add_coin, name='add_coin'),
    path('del_coin', views.del_coin, name='del_coin'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('del_transaction', views.del_transaction, name='del_transaction'),
    path('chart_data', views.get_chart_data, name='chart_data'),
]
