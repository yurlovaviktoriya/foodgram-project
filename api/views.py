import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from recipes.models import (
    User,
    Ingredient,
    Recipe,
    Subscription,
    FavoriteRecipe,
    Purchase
)


def get_ingredients(request):
    query_text = request.GET.get('query')
    ingredients = Ingredient.objects.filter(title__istartswith=query_text)
    if ingredients.exists():
        list_resp = []
        for ingredient in ingredients:
            dict_resp = {
                'title': ingredient.title,
                'dimension': ingredient.dimension
            }
            list_resp.append(dict_resp)
        return JsonResponse(list_resp, safe=False)
    json_resp = {"title": "", "dimension": ""}
    return JsonResponse(json_resp, safe=False)


@csrf_exempt
@requires_csrf_token
def add_subscription(request):
    cur_request = json.loads(request.body)
    author_id = cur_request.get('id', None)
    if author_id is not None:
        author = get_object_or_404(User, id=author_id)
        created = Subscription.objects.get_or_create(
            user=request.user,
            author=author
        )
        if created:
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})
    return JsonResponse({"success": False}, status=400)


@csrf_exempt
@requires_csrf_token
def remove_subscription(request, id):
    subscription = get_object_or_404(
        Subscription,
        user=request.user,
        author=id
    )
    subscription.delete()
    return JsonResponse({"success": True})


@csrf_exempt
@requires_csrf_token
def add_favorite(request):
    cur_request = json.loads(request.body)
    recipe_id = cur_request.get('id', None)
    if recipe_id is not None:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        created = FavoriteRecipe.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if created:
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})
    return JsonResponse({"success": False}, status=400)


@csrf_exempt
@requires_csrf_token
def remove_favorite(request, id):
    recipe = get_object_or_404(FavoriteRecipe, user=request.user, recipe=id)
    recipe.delete()
    return JsonResponse({"success": True})


@csrf_exempt
@requires_csrf_token
def add_purchase(request):
    cur_request = json.loads(request.body)
    recipe_id = cur_request.get('id', None)
    if recipe_id is not None:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        created = Purchase.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if created:
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})
    return JsonResponse({"success": False}, status=400)


@csrf_exempt
@requires_csrf_token
def remove_purchase(request, id):
    purchase = get_object_or_404(Purchase, user=request.user, recipe=id)
    purchase.delete()
    return JsonResponse({"success": True})
