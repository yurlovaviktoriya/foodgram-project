from django.db.models import Q

from recipes.models import Recipe, FavoriteRecipe, Purchase
    

def get_recipes_for_index(request):
    """This function is used to select recipes based on tags. The selected
    recipes will be displayed on the main page. By default there are three tags
    in the project: breakfast, dinner, supper. Filtration is carried out by one
    or several tags.

    Args:
        request: if the url contains 'tags' from the request, we get the tag
        values ​​and put them in list 'filter_tags'. Then the length of the list
        (variable 'len_of_filter_tags') can be equal to 1 ('breakfast' or
        'dinner' or 'supper'), 2 ('breakfast'and 'dinner' or 'breakfast' and
        'supper' or 'dinner' and 'supper') or 3 ('breakfast' and 'dinner' and
        'supper'). Depending on this, filtration occurs.

    Returns:
        QuerySet[]: list of recipe objects filtered by tags
    """
    if 'tags' not in str(request.get_full_path):
        recipes = Recipe.objects.all()
        return recipes
    filter_tags = request.GET.getlist('tags')
    len_of_filter_tags = len(filter_tags)
    if len_of_filter_tags == 1:
        recipes = Recipe.objects.filter(tags__name=filter_tags[0])
    elif len_of_filter_tags == 2:
        q = Q(tags__name=filter_tags[0]) | Q(tags__name=filter_tags[1])
        recipes = Recipe.objects.filter(q).distinct()
    elif len_of_filter_tags == 3:
        recipes = Recipe.objects.all()
    else:
        recipes = Recipe.objects.none()
    return recipes


def get_recipes_for_profile(request, username):
    """This function is used to select recipes based on tags. The selected
    recipes will be displayed on the user's profile page. By default there are
    three tags in the project: breakfast, dinner, supper. Filtration is carried
    out by one or several tags.

    Args:
        request: if the url contains 'tags' from the request, we get the tag
        values ​​and put them in list 'filter_tags'. Then the length of the list
        (variable 'len_of_filter_tags') can be equal to 1 ('breakfast' or
        'dinner' or 'supper'), 2 ('breakfast'and 'dinner' or 'breakfast' and
        'supper' or 'dinner' and 'supper') or 3 ('breakfast' and 'dinner' and
        'supper'). Depending on this, filtration occurs.

    Returns:
        QuerySet[]: list of recipe objects of one author filtered by tags
    """       
    if 'tags' not in str(request.get_full_path):
        recipes = Recipe.objects.filter(author__username=username)
        return recipes
    filter_tags = request.GET.getlist('tags')
    len_of_filter_tags = len(filter_tags)
    if len_of_filter_tags == 1:
        recipes = Recipe.objects.filter(
            tags__name=filter_tags[0],
            author__username=username
        )
    elif len_of_filter_tags == 2:
        q = (Q(tags__name=filter_tags[0], author__username=username) |
             Q(tags__name=filter_tags[1], author__username=username))
        recipes = Recipe.objects.filter(q).distinct()
    elif len_of_filter_tags == 3:
        recipes = Recipe.objects.filter(author__username=username)
    else:
        recipes = Recipe.objects.none()
    return recipes


def get_recipes_for_favorite(request):
    """This function is used to select recipes by tags. The selected
    recipes will be displayed on the favorite recipes page. By default there
    are three tags in the project: breakfast, dinner, supper. Filtration is
    carried out by one or several tags.

    Args:
        request: if the url contains 'tags' from the request, we get the tag
        values ​​and put them in list 'filter_tags'. Then the length of the list
        (variable 'len_of_filter_tags') can be equal to 1 ('breakfast' or
        'dinner' or 'supper'), 2 ('breakfast'and 'dinner' or 'breakfast' and
        'supper' or 'dinner' and 'supper') or 3 ('breakfast' and 'dinner' and
        'supper'). Depending on this, filtration occurs.

    Returns:
        QuerySet[]: list of favorite recipe objects filtered by tags
    """ 
    if 'tags' not in str(request.get_full_path):
        favorites = FavoriteRecipe.objects.filter(
            user__username=request.user
        )
    else:
        filter_tags = request.GET.getlist('tags')
        len_of_filter_tags = len(filter_tags)
        if len_of_filter_tags == 1:
            favorites = FavoriteRecipe.objects.filter(
                recipe__tags__name=filter_tags[0],
                user__username=request.user
            )
        elif len_of_filter_tags == 2:
            q = (Q(recipe__tags__name=filter_tags[0],
                   user__username=request.user) |
                 Q(recipe__tags__name=filter_tags[1],
                   user__username=request.user))
            favorites = FavoriteRecipe.objects.filter(q).distinct()
        elif len_of_filter_tags == 3:
            favorites = FavoriteRecipe.objects.filter(
                user__username=request.user
            )
        else:
            favorite = Recipe.objects.none()
            return favorite
    favorite_recipes = Recipe.objects.filter(
        favorite_recipes__in=favorites
    )       
    return favorite_recipes 


def get_favorite_recipes(request, recipes): 
    favorite_queryset = FavoriteRecipe.objects.filter(user=request.user)
    favorite_recipes = recipes.filter(
        favorite_recipes__in=favorite_queryset
    )
    return favorite_recipes


def get_purchases(request, recipes): 
    purchase_queryset = Purchase.objects.filter(user=request.user)
    purchases = recipes.filter(purchases__in=purchase_queryset)
    return purchases
    