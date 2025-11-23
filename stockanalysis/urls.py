from django.urls import path
from .views import *

urlpatterns = [
    path("stock/", stock_view, name="stock"),
    path("stock-autocomplete/",StockAutocomplete.as_view(), name="stock-autocomplete"),
    path('stock=detail/<int:pk>/',stock_detail_view,name='stock-detail'),
]
