from django.urls import resolve, Resolver404
from .models import MenuItem

def build_menu_tree(menu_items, current_url=None):

    menu_dict = {}  
    root_items = []  
    
    for item in menu_items:
        menu_dict[item.id] = {
            'item': item,           
            'children': [],        
            'is_active': False,     
            'is_expanded': False,   
            'parent': None          
        }
    
    for item in menu_items:
        node = menu_dict[item.id]
        
        if item.parent_id and item.parent_id in menu_dict:
            parent_node = menu_dict[item.parent_id]
            parent_node['children'].append(node)
            node['parent'] = parent_node
        else:
            root_items.append(node)
    
    if current_url:
        active_node = find_active_node(root_items, current_url)
        if active_node:
            mark_active_path(active_node)
    
    return root_items

def find_active_node(nodes, current_url):
    
    for node in nodes:
        if is_url_match(node['item'].get_absolute_url(), current_url):
            return node
        
        active_child = find_active_node(node['children'], current_url)
        if active_child:
            return active_child
    
    return None

def is_url_match(menu_url, current_url):
  
    
    if not menu_url or menu_url == '#':
        return False
    
    menu_url = menu_url.rstrip('/')
    current_url = current_url.rstrip('/')
    
    if menu_url == current_url:
        return True
    
    try:
        resolved_menu = resolve(menu_url)
        resolved_current = resolve(current_url)
        
        return (resolved_menu.url_name == resolved_current.url_name and 
                resolved_menu.args == resolved_current.args and 
                resolved_menu.kwargs == resolved_current.kwargs)
    except Resolver404:
        return False

def mark_active_path(active_node):
   
    active_node['is_active'] = True
    active_node['is_expanded'] = True
    
    for child in active_node['children']:
        child['is_expanded'] = True
    
    current = active_node
    while current.get('parent'):
        current['parent']['is_expanded'] = True
        current = current['parent']

def get_menu_data(menu_name, request):
    
    current_url = request.path
    
    menu_items = MenuItem.objects.filter(
        menu_name=menu_name
    ).select_related('parent').order_by('order', 'name')
    
    if not menu_items.exists():
        return []
    
    return build_menu_tree(menu_items, current_url)