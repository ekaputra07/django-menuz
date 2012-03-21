from django.db import models
from django.conf import settings

class Menuz(models.Model):
    title = models.CharField('Menu Title', max_length=50)
    position = models.CharField('Menu Position', max_length=100, choices=settings.AVAILABLE_MENUS, help_text='This is the position of the menu.')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu'

class MenuzItem(models.Model):
    menu = models.ForeignKey(Menuz)
    content_type = models.CharField(max_length=50)
    content_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=250)
    url = models.URLField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    order = models.IntegerField(blank=True, null=True, default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('order',)

