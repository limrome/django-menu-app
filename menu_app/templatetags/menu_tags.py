from django import template
from django.core.cache import cache
from menu_app.utils import get_menu_data

register = template.Library()

@register.inclusion_tag('menu_app/menu.html', takes_context=True)
def draw_menu(context, menu_name):
   
    request = context['request']
    
    cache_key = f'menu_{menu_name}_{request.path}'
    
    menu_tree = cache.get(cache_key)
    
    if menu_tree is None:
        menu_tree = get_menu_data(menu_name, request)
        cache.set(cache_key, menu_tree, 3600)
    
    return {
        'menu_tree': menu_tree,
        'menu_name': menu_name,
    }