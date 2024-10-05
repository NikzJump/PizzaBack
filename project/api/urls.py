from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('prods', views.get_prod),
    path('cart', views.get_cart),
    path('cart/<int:pk>', views.add_cart),
]
