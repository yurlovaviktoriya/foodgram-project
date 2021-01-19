from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.http import HttpResponse

from recipes.models import Recipe, Purchase, IngredientQuantity


def get_purchase_data(request):
    purchases = Purchase.objects.filter(user=request.user)
    recipes = Recipe.objects.filter(purchases__in=purchases)
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


def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'Список ингредиентов.pdf'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    data = get_purchase_data(request)
    pdfmetrics.registerFont(TTFont('dejavu-serif', 'dejavu-serif.ttf'))
    p.setFont('dejavu-serif', 15, leading=None)
    p.setFillColorRGB(0, 0, 255)
    p.drawString(180, 800, 'ПРОДУКТОВЫЙ ПОМОЩНИК')
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    p.drawString(208, 760, 'Список ингредиентов')
    x1 = 40
    y1 = 730
    num = 1
    for ingredient, quantity in data.items():
        p.setFont('dejavu-serif', 14, leading=None)
        p.drawString(x1, y1-12, f'{num}. {ingredient} - {quantity}')
        y1 -= 40
        num += 1 
    p.setTitle('Список ингредиентов')
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
