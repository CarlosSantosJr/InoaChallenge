from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date, timedelta
import yfinance as yf
from decimal import Decimal

from .models import UserAsset
from .models import AssetNews
from .models import AssetHistory
from .models import Asset


def index(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            asset_name = request.POST['asset_name']

            asset_info = yf.Ticker(asset_name)

            try:
                if asset_info.info.get('financialCurrency') is None:
                    messages.error(request, 'Não foi possível encontrar o ativo "{}" - se for uma ativo brasileiro tente adicionar .SA ao final.'.format(asset_name))
                else:
                    asset_list = Asset.objects.filter(name=asset_name)
                    if len(asset_list) == 0:
                        asset = Asset(name=asset_name, company_name=asset_info.info['longName'], currency=asset_info.info['financialCurrency'])
                        asset.save()

                        end_date = datetime.now(tz=None).strftime('%Y-%m-%d')
                        asset_history = asset_info.history(period='max', end=end_date, interval='1m')

                        for index, row in asset_history.iterrows():
                            timestamp = str(index)
                            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S%z')
                            timestamp = timestamp.replace(tzinfo=None)

                            if timestamp.weekday() == 4:
                                timestamp = timestamp + timedelta(days=3)
                            else:
                                timestamp = timestamp + timedelta(days=1)

                            asset_history = AssetHistory(asset=asset, timestamp=timestamp, value=row['Close'])
                            asset_history.save()

                    else:
                        asset = asset_list[0]

                    user_asset = UserAsset(
                        user=request.user,
                        asset=asset,
                        interval=1,
                        superior_limit=0.0,
                        inferior_limit=0.0
                    )
                    user_asset.save()

                    return redirect('asset_page', asset_id=asset.asset_id)
            except Exception as e:
                messages.error(request, 'Não foi possível adicionar o ativo "{}"'.format(asset_name))
                print(e)

        user_assets = UserAsset.objects.filter(user=request.user)
        prices = {}
        for user_asset in user_assets:
            prices[user_asset.asset.asset_id] = AssetHistory.objects.filter(asset=user_asset.asset).order_by('-timestamp')[0].value
        return render(
            request,
            'home/index.html',
            {"user_assets": user_assets, "asset_prices": prices}
        )

    else:
        return redirect('login')


def asset_page(request, asset_id):

    data = []
    labels = []

    if request.user.is_authenticated:
        try:
            if request.method == 'GET':
                time_query = request.GET.get('time')
                date_query = request.GET.get('date')
            else:
                time_query = request.POST.get('time')
                date_query = request.POST.get('date')

            if not time_query or not date_query:
                time_query = "1"
                date_query = "1"

            today = datetime.now(tz=None)
            date_interval = today - timedelta(days=(int(date_query)))

            asset = Asset.objects.filter(asset_id=asset_id)[0]
            user_asset = UserAsset.objects.filter(asset=asset, user=request.user)[0]
            asset_history = AssetHistory.objects.filter(asset=asset, timestamp__gte=date_interval)

            if request.method == 'POST':
                user_asset.interval = int(request.POST['interval'])
                user_asset.superior_limit = Decimal(request.POST['superior'].replace(',','.'))
                user_asset.inferior_limit = Decimal(request.POST['inferior'].replace(',','.'))
                user_asset.is_buy_sent = False
                user_asset.is_sell_sent = False

                user_asset.save()

            for i in range(0, len(asset_history), int(time_query)):
                if asset_history[i].timestamp <= today:
                    data.append(str(asset_history[i].value))
                    labels.append(asset_history[i].timestamp.strftime("%d/%m/%Y %H:%M"))

            return render(
                request,
                'asset_page/asset.html',{
                    'asset': asset,
                    'user_asset': user_asset,
                    'data': data,
                    'labels': labels,
                }
            )

        except Exception as e:
            print(e)
            messages.error(request, 'Não foi possível carregar informacoes do ativo')

    return redirect('home')


def remove_asset(request, asset_id):

    if request.user.is_authenticated:
        asset = Asset.objects.filter(asset_id=asset_id)[0]
        UserAsset.objects.filter(asset=asset, user=request.user)[0].delete()

    return redirect('home')
