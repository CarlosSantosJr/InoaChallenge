from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import yfinance as yf

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
                        asset = Asset(name=asset_name, company_name=asset_info.info['longName'])
                        asset.save()

                        end_date = datetime.now().strftime('%Y-%m-%d')
                        asset_history = asset_info.history(period='max',end=end_date,interval='1m')

                        for index, row in asset_history.iterrows():
                            asset_history = AssetHistory(asset=asset, timestamp=index, value=row['Close'])
                            asset_history.save()

                        for new in asset_info.news:
                            asset_new = AssetNews(
                                asset=asset,
                                headline=new['title'],
                                source=new['link'],
                                publish_date=datetime.fromtimestamp(new['providerPublishTime']).strftime('%Y-%m-%d')
                            )
                            asset_new.save()
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

    try:
        asset = Asset.objects.filter(asset_id=asset_id)[0]
        user_asset = UserAsset.objects.filter(asset=asset,user=request.user)[0]
        asset_news = AssetNews.objects.filter(asset=asset)
        asset_history = AssetHistory.objects.filter(asset=asset)

        return render(
            request,
            'asset_page/asset.html',
            {
                'asset': asset,
                'user_asset': user_asset,
                'asset_news': asset_news,
                'asset_history': asset_history,
            }
        )
    except:
        return redirect('home')


def remove_asset(request, asset_id):

    if request.user.is_authenticated:
        asset = Asset.objects.filter(asset_id=asset_id)[0]
        UserAsset.objects.filter(asset=asset, user=request.user)[0].delete()

    return redirect('home') 