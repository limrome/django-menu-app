from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _

class MenuItem(models.Model):
    name = models.CharField(_('name'), max_length=100)
    menu_name = models.CharField(
        _('menu name'), 
        max_length=100, 
    )
    
    parent = models.ForeignKey(
        'self',  
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',  
        verbose_name=_('parent')
    )
    
    url = models.CharField(
        _('URL'),
        max_length=200,
        blank=True,
    )
    named_url = models.CharField(
        _('named URL'),
        max_length=100,
        blank=True,
    )
    
    order = models.IntegerField(_('order'), default=0)
    
    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')
        ordering = ['menu_name', 'order', 'name']  
    
    def __str__(self):
        return f"{self.menu_name}: {self.name}"
    
    def get_absolute_url(self):
        
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                pass
        
        if self.url:
            return self.url
        
        return '#'  