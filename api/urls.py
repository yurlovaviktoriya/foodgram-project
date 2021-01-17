from django.urls import path

from . import views


urlpatterns = [
    path('ingredients/', views.get_ingredients, name='get_ingredients'),
    path('subscriptions', views.add_subscription, name='add_subscription'),
    path('subscriptions/<int:id>/', views.remove_subscription, name='remove_subscription'),
    path('favorites', views.add_favorite, name='add_favorite'),
    path('favorites/<int:id>/', views.remove_favorite, name='remove_favorite'),
    path('purchases', views.add_purchase, name='add_purchases'),
    path('purchases/<int:id>/', views.remove_purchase, name='remove_purchases'),
]