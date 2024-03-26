from background_task import background
from datetime import datetime
import yfinance as yf

from .models import AssetHistory
from .models import Asset

@background(schedule=60)
def update_asset_history():
    print('updated')
