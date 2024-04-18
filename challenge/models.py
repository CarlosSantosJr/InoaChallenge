from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Asset(models.Model):
  asset_id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=10)
  company_name = models.CharField(max_length=255, blank=True)
  currency = models.CharField(max_length=10, blank=True)


class UserAsset(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
  interval = models.IntegerField(blank=True)
  superior_limit = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
  inferior_limit = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
  last_udpate = models.DateTimeField(default=datetime.now)
  is_buy_sent = models.BooleanField(default=False)
  is_sell_sent = models.BooleanField(default=False)


class AssetHistory(models.Model):
  asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(default=datetime.now)
  value = models.DecimalField(max_digits=20, decimal_places=2)


class AssetNews(models.Model):
  asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
  news_id = models.AutoField(primary_key=True)
  headline = models.CharField(max_length=255)
  source = models.URLField()
  publish_date = models.DateTimeField()
  content = models.TextField(blank=True)
