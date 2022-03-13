from django.urls import path
from . import views
from store.views import Cart, CheckOut, OrderView
from django.contrib.auth import views as auth_views
from .middlewares.auth import auth_middleware


app_name = 'store'

urlpatterns = [
    path('store/', views.store, name='store'),
    path('signup/', views.Signup.as_view(), name='Signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

]
