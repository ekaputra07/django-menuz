from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from menuz.models import Menuz, MenuzItem
from menuz.registry import menuz
from menuz.utils import get_menu_by_position

register = template.Library()

@register.inclusion_tag('admin/menuz/menuz/menu_builder.html')
def menu_builder(object_id):
    """
    Menu Builder tags to use in django admin menu manager.
    """
    data = {
        'menu_id': object_id
        }

    #get available menus
    available_menus = []
    for meta in menuz.registry:
        source = {
            'type': meta['model'].__name__.lower(),
            'name' :meta['model']._meta.verbose_name_plural.title()
        }
        if meta.get('custom_source',''):
            source['queryset'] = meta['custom_source']()
        else:
            source['queryset'] = meta['model'].objects.all()
        available_menus.append(source)
    data['available_menus'] = available_menus

    #get Inner links
    if hasattr(settings, 'AVAILABLE_INNERLINKS'):
        data['innerlinks'] = getattr(settings, 'AVAILABLE_INNERLINKS')

    #get MenuItems
    menu_items = MenuzItem.objects.filter(menu__id=object_id).order_by('order')
    data['menu_items'] = menu_items

    return data



"""
Get Menu tag to use in front end and return value as context to give template designer
flexibility to style menu items them self.
returned value:
1. [varname]
2. [varname_title]
"""
@register.tag
def get_menu(parser, token):
    args = token.split_contents()

    if len(args) != 4:
        raise template.TemplateSyntaxError('get_menu tag usage not valid!. Usage : get_menu [menu_id] as [varname]')

    return MenuNode(args[1], args[3])

class MenuNode(template.Node):
    def __init__(self, position_id, varname):
        self.position_id = position_id
        self.varname = varname

    def render(self, context):
        title, items = get_menu_by_position(self.position_id)
        context[self.varname+'_title'] = title
        context[self.varname] = items
        return ''

@register.simple_tag
def list_menu(position_id):
    """
    Simple and generic menu tags to print menu items as a html list.
    this tags must be surrounded by <ul> tags.
    example:
    <ul>
    {% list_menu 'top_menu' %}
    </ul>
    """
    title, items = get_menu_by_position(position_id)
    output = []
    for item in items:
        output.append(u'<li><a href="%s" title="%s">%s</a></li>' % (item['url'], item['title'], item['title']))
    return u'\n'.join(output)

@register.filter
def truncatechars_right(value, length):
    if len(value) <= length:
        return value
    else:
        return u'%s...' % value[:length-3]

