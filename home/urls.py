from django.urls.conf import include
from home.views import home_view
from django.urls import path

urlpatterns = [
    path('', home_view, name='homepage'),
    path('donatore/', include('donatore.urls'), name='donatore'),
    path('associazione/', include('associazione.urls'), name='associazione'),
    path('accounts/', include('accounts.urls'), name='accounts'),
]