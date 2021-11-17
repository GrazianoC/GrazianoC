from .views import FoodDistListView, TemporaryOrder, CartListView, CartDeleteItem, InviaOrdine, Dashboard
from django.urls import path

urlpatterns = [
    path('foodlistas/', FoodDistListView.as_view(), name='foodlistas'),
    path('carrello/', CartListView.as_view(), name='carrello'),
    path('carrellodel/<int:pk>', CartDeleteItem, name='carrellodel'),
    path('tempord/<int:pk>', TemporaryOrder, name='tempord'),
    path('creaordine/', InviaOrdine, name='creaordine'),
    path('dashboarda/', Dashboard, name='dashboarda'),
]
