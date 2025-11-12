from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_name', 'parent', 'order', 'url', 'named_url')
    
    list_filter = ('menu_name',)
    
    search_fields = ('name', 'menu_name', 'url', 'named_url')
    
    list_editable = ('order',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'menu_name', 'parent', 'order')
        }),
        ('URL Settings', {
            'fields': ('url', 'named_url'),
            'description': 'You can use either explicit URL or named URL pattern. Named URL has priority.'
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        
        form = super().get_form(request, obj, **kwargs)
        
        if obj and obj.menu_name:
            
            form.base_fields['parent'].queryset = MenuItem.objects.filter(
                menu_name=obj.menu_name
            ).exclude(pk=obj.pk)  
        
        return form

admin.site.register(MenuItem, MenuItemAdmin)