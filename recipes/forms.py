from django.forms import ModelForm, Textarea, FileInput

from .models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'name',
            'cook_time',
            'description',
            'image',
        )
        labels = {
            'name': 'Название рецепта',
            'tag': 'Tэги',
            'cook_time': 'Время приготовления',
            'description': 'Описание',
            'image': 'Загрузить фото',
        }
        widgets = {
            'description': Textarea(attrs={
                'name': 'description',
                'id': 'id_description',
                'rows': '8',
                'class': 'form__textarea'
            }),
            'image': FileInput(attrs={
                'name': 'file',
                'id': 'id_file',
                'class': 'form__file'
            })
        }
       