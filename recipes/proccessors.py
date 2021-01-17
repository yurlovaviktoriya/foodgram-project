from decimal import Decimal
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse

from .models import (
    Recipe,
    FavoriteRecipe,
    Purchase,
    IngredientQuantity,
    Ingredient,
    Tag
)


class GetRecipes():
    
    @staticmethod
    def get_recipes_for_index(request):
        if 'tags' not in str(request.get_full_path):
            recipes = Recipe.objects.all()
        else:
            filter_tags = request.GET.getlist('tags')
            len_of_filter_tags = len(filter_tags)
            if  len_of_filter_tags == 1:
                recipes = Recipe.objects.filter(tag__slug=filter_tags[0])
            elif len_of_filter_tags == 2:
                q = Q(tag__slug=filter_tags[0]) | Q(tag__slug=filter_tags[1])
                recipes = Recipe.objects.filter(q).distinct()
            elif len_of_filter_tags == 3:
                recipes = Recipe.objects.all()
        return recipes
    
    
    @staticmethod
    def get_recipes_for_profile(request, username):        
        if 'tags' not in str(request.get_full_path):
            recipes = Recipe.objects.filter(author__username=username)
        else:
            filter_tags = request.GET.getlist('tags')
            len_of_filter_tags = len(filter_tags)
            if  len_of_filter_tags == 1:
                recipes = Recipe.objects.filter(
                    tag__slug=filter_tags[0],
                    author__username=username
                )
            elif len_of_filter_tags == 2:
                q = Q(tag__slug=filter_tags[0], author__username=username) | \
                    Q(tag__slug=filter_tags[1], author__username=username)
                recipes = Recipe.objects.filter(q).distinct()
            elif len_of_filter_tags == 3:
                recipes = Recipe.objects.filter(author__username=username)
        return recipes


    @staticmethod
    def get_recipes_for_favorite(request): 
        if 'tags' not in str(request.get_full_path):
            favorites = FavoriteRecipe.objects.filter(
                user__username=request.user
            )
        else:
            filter_tags = request.GET.getlist('tags')
            len_of_filter_tags = len(filter_tags)
            if  len_of_filter_tags == 1:
                favorites = FavoriteRecipe.objects.filter(
                    recipe__tag__slug=filter_tags[0],
                    user__username=request.user
                )
            elif len_of_filter_tags == 2:
                q = Q(
                    recipe__tag__slug=filter_tags[0],
                    user__username=request.user) | \
                    Q(
                    recipe__tag__slug=filter_tags[1],
                    user__username=request.user)
                favorites = FavoriteRecipe.objects.filter(q).distinct()
            elif len_of_filter_tags == 3:
                favorites = FavoriteRecipe.objects.filter(
                    user__username=request.user
                )
        favorite_recipes = Recipe.objects.filter(
            favorite_recipe__in=favorites
        )       
        return favorite_recipes 
    
    
    @staticmethod
    def get_favorite_recipes(request, recipes): 
        favorite_queryset = FavoriteRecipe.objects.filter(user=request.user)
        favorite_recipes = recipes.filter(
            favorite_recipe__in=favorite_queryset
        )
        return favorite_recipes
    
    
    @staticmethod
    def get_purchases(request, recipes): 
        purchase_queryset = Purchase.objects.filter(user=request.user)
        purchases = recipes.filter(purchase__in=purchase_queryset)
        return purchases
        
        
class SaveRecipe():
    
    @staticmethod                        
    def extract_ingredients(request):
        ingredients={}
        for key in request.POST:
            if key.startswith('nameIngredient'):
                ingredient_value = key[15:]
                ingredients[request.POST[key]] = request.POST[
                    f'valueIngredient_{ingredient_value}']
        return ingredients
    
        
    @staticmethod     
    def extract_tags(request):
        tags = []
        name_of_tags = ('breakfast', 'dinner', 'supper',)
        for key in request.POST:
            if key in name_of_tags and request.POST[key] == 'on':
                tags.append(key)         
        return tags

    
    @staticmethod
    def save_tags(request, recipe):
        tags = SaveRecipe.extract_tags(request)
        for tag in tags:
            tag_add = Tag.objects.get(name=tag)
            recipe.tag.add(tag_add)
    
    
    @staticmethod
    def save_ingredients(request, recipe):   
        ingredients = SaveRecipe.extract_ingredients(request)
        num_of_ingredients = []
        for title, quantity in ingredients.items():
            num_of_ingredients.append(
                IngredientQuantity(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(title=title),
                    quantity=Decimal(quantity.replace(',','.'))
                )
            )
        IngredientQuantity.objects.bulk_create(num_of_ingredients)   


class GetPDF():

    @staticmethod 
    def get_purchase_data(request):
        purchases = Purchase.objects.filter(user=request.user)
        recipes = Recipe.objects.filter(purchase__in=purchases)
        ingredients = {}
        for recipe in recipes:
            ingredient_queryset = IngredientQuantity.objects.filter(
                recipe=recipe
            )
            for item in ingredient_queryset:
                if item.ingredient in ingredients:
                    ingredients[item.ingredient] += item.quantity
                else:
                    ingredients[item.ingredient] = item.quantity
        return ingredients

    @staticmethod 
    def generate_pdf(request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'Список ингредиентов.pdf'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        data = GetPDF.get_purchase_data(request)
        pdfmetrics.registerFont(TTFont('dejavu-serif', 'dejavu-serif.ttf'))
        p.setFont('dejavu-serif', 15, leading=None)
        p.setFillColorRGB(0,0,255)
        p.drawString(180,800, 'ПРОДУКТОВЫЙ ПОМОЩНИК')
        p.line(0,780,1000,780)
        p.line(0,778,1000,778)
        p.drawString(208,760, 'Список ингредиентов')
        x1 = 40
        y1 = 730
        num = 1
        for ingredient, quantity in data.items():
            p.setFont('dejavu-serif', 14, leading=None)
            p.drawString(x1,y1-12, f'{num}. {ingredient} - {quantity}')
            y1 -= 40
            num += 1 
        p.setTitle('Список ингредиентов')
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    