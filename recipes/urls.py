from django.urls import path

from . import views, proccessors


urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('recipe/<str:username>/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<str:username>/<int:id>/delete/', views.delete_recipe, name='recipe_delete'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('recipe/favorite/', views.favorite_recipes, name='favorite_recipes'),
    path('my-subscriptions/', views.subscriptions, name='my_subscriptions'),
    path('my-purchases/', views.purchases, name='my_purchases'),
    path('purchase/<str:username>/<int:id>/delete/', views.delete_purchase, name='purchase_delete'),
    path('generate_pdf/', proccessors.GetPDF.generate_pdf, name='generate_pdf'),
]