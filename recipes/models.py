from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование ингредиента'
    )
    dimension = models.CharField(
        max_length=20,
        verbose_name='Единица измерения'
    )
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'dimension',),
                name='unique_ingredient'
            ),
        ]

    def __str__(self):
        return f'{self.title} ({self.dimension}.)'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    description = models.CharField(
        max_length=3000,
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientQuantity',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Tэг'
    )
    cook_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Количество'
    )
    
    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецептах'
    
    def __str__(self):
        return f'Количество {self.ingredient} в рецепте"{self.recipe}"'

     
class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь',
        db_index=False
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепт',
        db_index=False
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite_recipe'
            ),
        ]

    def __str__(self):
        return f'Избранный рецепт ({self.user})'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь',
        db_index=False
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Рецепт',
        db_index=False
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_purchase'
            ),
        ]

    def __str__(self):
        return f'Покупка ({self.user})'
    
    
class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        db_index=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Интересный автор',
        db_index=False
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscription'
            ),
        ]

    def __str__(self):
        return f'Подписка ({self.user})'


class TagName(models.TextChoices):
        BREAKFAST = 'breakfast', 'завтрак'
        DINNER = 'dinner', 'обед'
        SUPPER = 'supper', 'ужин' 


class TagColor(models.TextChoices):
        BREAKFAST = 'orange'
        DINNER = 'green'
        SUPPER = 'purple'


class Tag(models.Model):
    name = models.CharField(
        max_length = 20,
        unique=True,
        choices=TagName.choices,
        verbose_name='Тэг',
    )
    color = models.CharField(
        max_length = 20,
        unique=True,
        choices=TagColor.choices,
        verbose_name='Цвет тэга в шаблоне',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        
    def __str__(self):
        return self.name
    