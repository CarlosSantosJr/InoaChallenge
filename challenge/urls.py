from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('asset/<int:asset_id>', views.asset_page, name='asset_page'),
    path('asset/<int:asset_id>/remove', views.remove_asset, name='remove_asset')
]
