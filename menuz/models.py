from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def get_available_menu():
    """
    Get available menus at project settings.py and convert to choices tuple format
    for used by admin panel menu selection.
    """
    try:
        available_menus = settings.AVAILABLE_MENUS
    except AttributeError:
        return ((None, _('No menu defined.')),)
    else:
        menus = ((menu['id'], menu['title']) for menu in available_menus)
        return menus
        

class Menuz(models.Model):
    title = models.CharField(_('Menu Title'), max_length=50)
    position = models.CharField(_('Menu Position'), max_length=100, 
                        choices=get_available_menu(),
                        help_text=_('This is position of the menu.'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')


class MenuzItem(models.Model):
    menu = models.ForeignKey(Menuz)
    content_type = models.CharField(max_length=50)
    content_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=250)
    url = models.URLField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    order = models.IntegerField(blank=True, null=True, default=100)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('order',)

