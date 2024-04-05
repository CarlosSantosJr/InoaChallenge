from django.db import models
from django.utils import timezone
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


class AssetHistory(models.Model):
  asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(default=timezone.now)
  value = models.DecimalField(max_digits=20, decimal_places=2)


class AssetNews(models.Model):
  asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
  news_id = models.AutoField(primary_key=True)
  headline = models.CharField(max_length=255)
  source = models.URLField()
  publish_date = models.DateTimeField()
  content = models.TextField(blank=True)
