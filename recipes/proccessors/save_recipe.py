from decimal import Decimal

from recipes.models import Tag, Ingredient, IngredientQuantity

                       
def extract_ingredients(request):
    UNUSED_DATA_THRESHOLD = 15
    ingredients={}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingredient_value = key[UNUSED_DATA_THRESHOLD:]
            ingredients[request.POST[key]] = request.POST[
                f'valueIngredient_{ingredient_value}']
    return ingredients

   
def extract_tags(request):
    tags = []
    name_of_tags = ('breakfast', 'dinner', 'supper',)
    for key in request.POST:
        if key in name_of_tags and request.POST.get(key) == 'on':
            tags.append(key)         
    return tags


def save_tags(request, recipe):
    tags = extract_tags(request)
    for tag in tags:
        tag_add = Tag.objects.get(name=tag)
        recipe.tags.add(tag_add)


def save_ingredients(request, recipe):   
    ingredients = extract_ingredients(request)
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
     