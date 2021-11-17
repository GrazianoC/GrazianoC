from .views import FoodInsert, FoodListView, FoodEdit, FoodDelete, FoodDetail, AddressListView, AddressInsert, FoodWhat, Dashboard, OrderListView
from django.urls import path

urlpatterns = [
    path('address/', AddressListView.as_view(), name='address'),
    path('newaddress/',AddressInsert.as_view(), name='newaddress'),
    path('foodlist/', FoodListView.as_view(), name='foodlist'),
    path('foodwhat/', FoodWhat, name='foodwhat'),
    path('newfood/', FoodInsert.as_view(), name='newfood'),
    path('editfood/<int:pk>', FoodEdit.as_view(), name='editfood'),
    path('deletefood/<int:pk>', FoodDelete.as_view(), name='deletefood'),
    path('detailfood/<int:pk>', FoodDetail.as_view(), name='detailfood'),
    path('orderlist/', OrderListView.as_view(), name='orderlist'),
    path('dashboard/', Dashboard, name='dashboard'),
]
