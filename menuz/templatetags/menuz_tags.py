from django import template
from django.core.urlresolvers import reverse
from django.conf import settings

from menuz.models import Menuz, MenuzItem
from menuz.registry import menuz
from menuz.utils import get_menu_by_position, get_menu_options
from menuz.utils import get_menu_components, count_menu_children

register = template.Library()

########################## This tag is for Django-Menuz Admin Panel ###########

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

    return data

###############################################################################

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
        raise template.TemplateSyntaxError('get_menu tag usage not valid!.\
                                 Usage : get_menu [menu_id] as [varname]')

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

# recursively render menu children
def render_menu_children(request, parent, items, menu_tag):
    childs = []
    output = []
        
    for menu in items:
        if menu['parent_id'] == parent['id']:
            childs.append(menu)

    if childs:
        output.append('<%s class="ul_sublevel">' % menu_tag)
        for menu in childs:
        
            current_class = ''
            if request.path == menu.get('url'):
                current_class = 'current'

            output.append('<li class="li_sublevel menu_%s %s">' % (menu['id'], current_class))
            output.append('<a href="%s" title="%s">%s</a>' % (menu['url'], menu['title'], menu['title']))
            output.append(render_menu_children(request, menu, items, menu_tag))
            output.append('</li>')
        output.append('</%s>' % menu_tag)
        
    return u'\n'.join(output)


@register.simple_tag(takes_context=True)
def list_menu(context, position_id):
    """
    Simple and generic menu tags to print menu items as a html list.
    example:
    {% list_menu 'top_menu' %}
    """ 
    request  = context.get('request')

    title, items = get_menu_by_position(position_id)
    menu_tag, menu_class, before_link, after_link = get_menu_components(position_id)
    
    output = []
    output.append('<%s class="ul_toplevel %s">' % (menu_tag, menu_class))
    top_menu_count = count_menu_children(items, 0)
    
    counter = 0
    for menu in items:
        if menu['parent_id'] == 0:
        
            current_class = ''
            if request.path == menu.get('url'):
                current_class = 'current'

            if counter == 0:
                output.append('<li class="li_toplevel first menu_%s %s">' % (menu['id'], current_class))
            elif counter == top_menu_count-1:
                output.append('<li class="li_toplevel last menu_%s %s">' % (menu['id'], current_class))
            else:
                output.append('<li class="li_toplevel menu_%s %s">' % (menu['id'], current_class))
            output.append('%s<a href="%s" title="%s">%s</a>%s' % (before_link, menu['url'], menu['title'], menu['title'], after_link))
            output.append(render_menu_children(request, menu, items, menu_tag))
            output.append('</li>')
            counter += 1
            
    output.append('</%s>' % menu_tag)
          
    return u'\n'.join(output)


@register.filter
def truncatechars_right(value, length):
    if len(value) <= length:
        return value
    else:
        return u'%s...' % value[:length-3]

