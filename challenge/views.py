from django.core.checks import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import yfinance as yf

from .models import UserAsset
from .models import AssetNews
from .models import Asset


def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            asset_name = request.POST['asset_name']

            asset_info = yf.Ticker(asset_name)

            try:
                if (asset_info.info['financialCurrency'] == None):
                        raise Exception("Not able to find ticker! Try again.")

                asset = Asset(name=asset_name, company_name=asset_info.info['longName'])
                asset.save()

                user_asset = UserAsset(
                    user=request.user,
                    asset=asset,
                    interval=1,
                    superior_limit=0.0,
                    inferior_limit=0.0
                )
                user_asset.save()

                # end_date = datetime.now().strftime('%Y-%m-%d')
                # asset_history = asset_info.history(period='max',end=end_date,interval='1m')

                # print("HISTORY")
                # print(asset_history)
                # for history_value in asset_history:

                for new in asset_info.news:
                    asset_new = AssetNews(asset=asset, headline=new['title'], source=new['link'], publish_date="2024-03-25")
                    asset_new.save()


                return redirect('asset_page', asset_id=asset.asset_id)
            except Exception as e:
                print("Not possible to add", e)

        user_assets = UserAsset.objects.filter(user=request.user)
        return render(
            request,
            'home/index.html',
            {"user_assets": user_assets}
        )

    else:
        return redirect('login')


def asset_page(request, asset_id):
    try:
        asset = Asset.objects.filter(asset_id=asset_id)[0]
        user_asset = UserAsset.objects.filter(asset=asset,user=request.user)[0]
        asset_news = AssetNews.objects.filter(asset=asset)

        return render(
            request,
            'asset_page/asset.html',
            {
                'asset': asset,
                'user_asset': user_asset,
                'asset_news': asset_news,
            }
        )
    except:
        return redirect('home')
