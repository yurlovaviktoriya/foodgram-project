from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import RecipeForm
from .proccessors import GetRecipes, SaveRecipe
from .models import (
    Recipe,
    User,
    Ingredient,
    IngredientQuantity,
    Tag,
    FavoriteRecipe,
    Subscription,
    Purchase
)
 

def index(request):
    recipes = GetRecipes.get_recipes_for_index(request)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    indx = True
    tags = Tag.objects.all()
    if request.user.is_authenticated:
        num_purchases = Purchase.objects.filter(user=request.user).count()
        favorite_recipes = GetRecipes.get_favorite_recipes(request, recipes)
        purchases = GetRecipes.get_purchases(request, recipes)
        context = {
            'num_purchases': num_purchases,
            'tags': tags,
            'page': page,
            'paginator': paginator,
            'indx': indx,
            'favorite_recipes': favorite_recipes,
            'purchases': purchases
        }
        return render(request, 'index.html', context)
    context = {
        'tags': tags,
        'page': page,
        'paginator': paginator,
        'indx': indx
    }
    return render(request, 'index.html', context)


def profile(request, username):
    recipes = GetRecipes.get_recipes_for_profile(request, username)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    indx = True
    tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        num_purchases = Purchase.objects.filter(user=request.user).count()
        subscription = Subscription.objects.filter(
            user=request.user,
            author=author
        ).exists()
        favorite_recipes = GetRecipes.get_favorite_recipes(request, recipes)
        purchases = GetRecipes.get_purchases(request, recipes)
        context = {
            'num_purchases': num_purchases,
            'subscription': subscription,
            'tags': tags,
            'author': author,
            'page': page,
            'paginator': paginator,
            'indx': indx,
            'favorite_recipes': favorite_recipes,
            'purchases': purchases,
        }
        return render(request, 'profile.html', context)
    context = {
        'tags': tags,
        'author': author,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'profile.html', context)


@login_required
def favorite_recipes(request):
    favorite_recipes = GetRecipes.get_recipes_for_favorite(request)
    paginator = Paginator(favorite_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    favorite = True
    tags = Tag.objects.all()
    num_purchases = Purchase.objects.filter(user=request.user).count()
    purchases = GetRecipes.get_purchases(request, favorite_recipes)
    context = {
        'tags': tags,
        'page': page,
        'paginator': paginator,
        'favorite': favorite,
        'favorite_recipes': favorite_recipes,
        'num_purchases': num_purchases,
        'purchases': purchases,
    }
    return render(request, 'favorite.html', context)


@login_required
def new_recipe(request):
    is_edit = False
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            new_recipe = Recipe.objects.get(id=recipe.id)
            SaveRecipe.save_tags(request, new_recipe)
            SaveRecipe.save_ingredients(request, recipe)
            return redirect(
                'recipe',
                username=request.user.username,
                recipe_id=recipe.id
            )
        context = {
            'form': form,
            'is_edit': is_edit
        }
        return render(request, 'new_recipe.html', context)    
    form = RecipeForm()
    tags = Tag.objects.all()
    new = True
    context = {
            'form': form,
            'is_edit': is_edit,
            'tags': tags,
            'new': new
        }
    return render(request, 'new_recipe.html', context)


@login_required
def recipe_edit(request, username, recipe_id):
    is_edit = True
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.save()
        recipe.tag.clear()
        SaveRecipe.save_tags(request, recipe)
        recipe.ingredientquantity_set.all().delete()
        SaveRecipe.save_ingredients(request, recipe)
        return redirect(
            'recipe',
            username=recipe.author.username,
            recipe_id=recipe.id
        )
    if recipe.author == request.user:
        tags = Tag.objects.all()
        tags_of_recipe = recipe.tag.all()
        ingredients_of_recipe = recipe.ingredientquantity_set.all()
        context = {
            'form': form,
            'recipe': recipe,
            'tags': tags,
            'tags_of_recipe': tags_of_recipe,
            'ingredients_of_recipe': ingredients_of_recipe,
            'is_edit': is_edit
        }
        return render( request, 'new_recipe.html', context)
    return redirect(
        'recipe',
        username=recipe.author.username,
        recipe_id=recipe.id
    )


@login_required
def delete_recipe(request, username, id):
    recipe = get_object_or_404(Recipe, pk=id, author__username=username)
    if recipe.author == request.user:
        recipe.delete()
        return redirect('profile', username=request.user)
    return redirect(
        'recipe',
        username=recipe.author.username,
        recipe_id=recipe.id
    )


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, author=author, id=recipe_id)
    indx = True
    if request.user.is_authenticated:
        num_purchases = Purchase.objects.filter(user=request.user).count()
        favorite_recipe = FavoriteRecipe.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
        subscription = Subscription.objects.filter(
            user=request.user,
            author__username=username
        ).exists()
        purchase = Purchase.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
        context = {
            'author': author,
            'recipe': recipe,
            'num_purchases': num_purchases,
            'favorite_recipe': favorite_recipe,
            'subscription': subscription,
            'purchase': purchase,
            'indx': indx
        }
        return render(request, 'recipe.html', context)
    context = {'author': author, 'recipe': recipe, 'indx': indx}
    return render(request, 'recipe.html', context)


@login_required
def subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    paginator = Paginator(subscriptions, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    follow = True
    num_purchases = Purchase.objects.filter(user=request.user).count()
    context = {
        'page': page,
        'paginator': paginator,
        'follow': follow,
        'num_purchases': num_purchases,
    }
    return render(request, 'subscription.html', context)


@login_required
def purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    num_purchases = purchases.count()
    purchase = True
    context = {
        'purchases': purchases,
        'num_purchases': num_purchases,
        'purchase': purchase,
        
    }
    return render(request, 'purchases.html', context)


@login_required
def delete_purchase(request, username, id):
    purchase = get_object_or_404(Purchase, pk=id, user__username=username)
    if purchase.user == request.user:
        purchase.delete()
        return redirect('my_purchases')
    return render(
        request, 
        'misc/404.html', 
        {'path': request.path}, 
        status=404
    )


def page_not_found(request, exception):
    return render(
        request, 
        'misc/404.html', 
        {'path': request.path}, 
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
