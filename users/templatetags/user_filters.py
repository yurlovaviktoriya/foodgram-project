from django import template
from django.utils.http import urlencode

register = template.Library()


@register.filter 
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def get_tags(value):
    return value.getlist('tags')


@register.filter
def create_tag_link(request, tag):
    query = request.GET.copy()
    if 'tags' not in str(request.get_full_path):
        tags = ['breakfast', 'dinner', 'supper']
        tags.remove(tag.slug)
        query.setlist('tags', tags)
    elif tag.slug in request.GET.getlist('tags'):
        tags = query.getlist('tags')
        tags.remove(tag.slug)
        query.setlist('tags', tags)
    else:
        query.appendlist('tags', tag.slug)
    return query.urlencode()


@register.filter
def format_count(count, word):
    count -= 3
    if count > 0:
        remainder_ten = count % 10
        remainder_hundred = count % 100
        if remainder_ten == 0:
            word += 'ов'
        elif remainder_ten == 1 and remainder_hundred != 11:
            word += ''
        elif remainder_ten < 5 and remainder_hundred not in [11, 12, 13, 14]:
            word += 'а'
        else:
            word += 'ов'
        return f'Ещё {count} {word}...'
    return f''


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    if query.get ('page'):
        query.pop ('page')
    query.update(kwargs)
    return query.urlencode()
