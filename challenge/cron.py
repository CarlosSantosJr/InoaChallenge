from datetime import datetime, timedelta
from django.core.mail import send_mail
import yfinance as yf

from .models import AssetHistory
from .models import UserAsset
from .models import Asset


def update_asset_history():
    print("-"*40)
    print("task - update_asset_history: Started")

    today = datetime.now()
    assets = Asset.objects.all()

    for asset in assets:
        history_prices = AssetHistory.objects.filter(asset=asset, timestamp__day=today.day, timestamp__month=today.month, timestamp__year=today.year)
        for price in history_prices:
            print(price.timestamp)

        if not (len(history_prices) > 0):
            asset_info = yf.Ticker(asset.name.rstrip())
            end_date = datetime.now(tz=None).strftime('%Y-%m-%d')
            asset_history = asset_info.history(period='max', end=end_date, interval='1m')

            if today.weekday() == 1:
                today = today - timedelta(days=3)
            else:
                today = today - timedelta(days=1)

            for index, row in asset_history.iterrows():
                timestamp = str(index)
                timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S%z')
                timestamp = timestamp.replace(tzinfo=None)

                if timestamp.date() == today.date():
                    if timestamp.weekday() == 4:
                        timestamp = timestamp + timedelta(days=3)
                    else:
                        timestamp = timestamp + timedelta(days=1)

                    asset_history = AssetHistory(asset=asset, timestamp=timestamp, value=row['Close'])
                    asset_history.save()

    print("task - update_asset_history: End")
    print("-"*40)


def check_asset_prices():
    print("-"*40)
    print("task - check_asset_prices: Started")

    all_user_assets = UserAsset.objects.all()

    for user_asset in all_user_assets:
        if user_asset.inferior_limit != 0 or user_asset.superior_limit != 0:
            print(f"user: {user_asset.user.username} - asset: {user_asset.asset.name}")
            print(f"last update: {user_asset.last_udpate} - interval: {user_asset.interval}")
            print(f"sum: {user_asset.last_udpate + timedelta(minutes=user_asset.interval)}")
            print(f"time now: {datetime.now()}")
            if (user_asset.last_udpate + timedelta(minutes=user_asset.interval)) <= datetime.now():
                print("Updating")
                user_asset.last_udpate = datetime.now()

                asset_price = AssetHistory.objects.filter(timestamp__range=[datetime.now() - timedelta(minutes=1),datetime.now() + timedelta(minutes=1)], timestamp__minute=datetime.now().minute)[0]
                print(f"Horario do preco: {asset_price.timestamp}")
                print(f"Preco: {asset_price.value}")
                print(f"lower range: {user_asset.inferior_limit} - upper range: {user_asset.superior_limit}")

                if asset_price.value >= user_asset.inferior_limit and asset_price.value <= user_asset.superior_limit and not user_asset.is_buy_sent:
                    print("Enviando email de compra")

                    send_mail(
                        f"{user_asset.asset.name} - Compra de Ativo",
                        f"Está na hora de efetuar a compra do ativo {user_asset.asset.name}, ele está dentro do tunel definido",
                        None,
                        [user_asset.user.email],
                        fail_silently=False,
                    )

                    user_asset.is_buy_sent = True

                if asset_price.value >= user_asset.superior_limit and not user_asset.is_sell_sent:
                    print("Enviando email de venda")

                    send_mail(
                        f"{user_asset.asset.name} - Venda de Ativo",
                        f"Está na hora de efetuar a venda do ativo {user_asset.asset.name}, ele está fora do tunel definido",
                        None,
                        [user_asset.user.email],
                        fail_silently=False,
                    )

                    user_asset.is_sell_sent = True

                user_asset.save()

    print("task - check_asset_prices: End")
    print("-"*40)
