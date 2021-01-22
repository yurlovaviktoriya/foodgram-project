from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

from recipes.models import Tag, Ingredient, IngredientQuantity


UNUSED_DATA_THRESHOLD = 15

                      
def extract_ingredients(request):
    ingredients={}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            list_value = []
            num = key[UNUSED_DATA_THRESHOLD:]
            list_value.append(request.POST[f'valueIngredient_{num}'])
            list_value.append(request.POST[f'unitsIngredient_{num}'])
            ingredients[request.POST[key]] = list_value
    return ingredients

   
def extract_tags(request):
    tags = []
    name_of_tags = ('breakfast', 'dinner', 'supper',)
    for key in request.POST:
        if key in name_of_tags and request.POST.get(key) == 'on':
            tags.append(key)         
    return tags


def check_query(request):
    tag_or_ingredient_empty = []
    tags_from_query = extract_tags(request)
    if not tags_from_query:
        tag_or_ingredient_empty.append('tag_empty')
    ingredients_from_query = extract_ingredients(request)
    if not bool(ingredients_from_query):
        tag_or_ingredient_empty.append('ingredient_empty')
    return tag_or_ingredient_empty, tags_from_query, ingredients_from_query 


def save_tags(request, recipe, tags):
    for tag in tags:
        tag_add = Tag.objects.get(name=tag)
        recipe.tags.add(tag_add)


def save_ingredients(request, recipe, ingredients):   
    num_of_ingredients = []
    unknown_ingredients = []
    success = None
    for title, value_list in ingredients.items():
        try:
            num_of_ingredients.append(
                IngredientQuantity(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(title=title),
                    quantity=Decimal(value_list[0].replace(',','.'))
                )
            )
        except Ingredient.DoesNotExist:
            success = False
            unknown_ingredients.append(title)
    if unknown_ingredients:    
        return success, num_of_ingredients, unknown_ingredients       
    IngredientQuantity.objects.bulk_create(num_of_ingredients)
    success = True
    return success, None, None
     