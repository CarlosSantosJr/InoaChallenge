from datetime import datetime
import yfinance as yf

from models import AssetHistory
from models import Asset

def update_asset_history():
    assets = Asset.objects.all()

    asset_list_codes = ''

    for asset in assets:
        asset_list_codes = asset_list_codes + ' ' + asset.name
    asset_list_codes = asset_list_codes.strip()
