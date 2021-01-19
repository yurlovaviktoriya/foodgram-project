from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    IngredientQuantity,
    FavoriteRecipe,
    Purchase,
    Subscription,
    Tag
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'dimension',
    )
    list_filter = ('title',)
    empty_value_display = '-пусто-'
    
    
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'count',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    empty_value_display = '-пусто-'
    
    def count(self, obj):
        return obj.favorite_recipes.count()
    count.short_description = 'Количество добавлений в избранное'


admin.site.register(IngredientQuantity)
admin.site.register(FavoriteRecipe)
admin.site.register(Purchase)
admin.site.register(Subscription)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
