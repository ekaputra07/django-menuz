from django.core.urlresolvers import reverse
from menuz.models import Menuz, MenuzItem
from menuz.registry import menuz
from menuz.registry import get_menuz_object_model
from django.conf import settings

# used in conjunction with egocms app
# part of Egomedia Bali's inhouse CMS project
egosetting_available = True
try:
    from egosettings.egosetting import get_setting
except ImportError:
    egosetting_available = False

def get_menu_by_position(position):
    """
    Return all menu items based on position ID.
    """
    menu_title = ''
    all_items = []
    #get all menu items
    
    def has_parent(obj):
        if obj.parent:
            return obj.parent.id
        return 0
    
    try:
        menu = Menuz.objects.get(position__exact=position)
        menu_title = menu.title
        menu_contents = menu.menuzitem_set.all()
        #get all menu data, and return title and links only 
        
        for obj in menu_contents:
            if obj.content_type == 'custom' or obj.content_type == 'innerlink':
                all_items.append({'id': obj.id, 'url': obj.url, 'title': obj.title, 'parent_id': has_parent(obj)})
            else:
                if get_menuz_object_model(obj.content_type):
                    model = get_menuz_object_model(obj.content_type)
                    try:
                        item = model.objects.get(pk=obj.content_id)
                        
                        # works with egocms
                        # this will check if current page setted as homepage_id
                        # if yes, then display site base url
                        if egosetting_available:
                            homepage_id = get_setting('site_homepage')
                            if homepage_id == item.id:
                                all_items.append({'id': obj.id, 'url': reverse('index'), 'title': obj.title, 'parent_id': has_parent(obj)})
                            else:
                                all_items.append({'id': obj.id, 'url': item.get_absolute_url(), 'title': obj.title, 'parent_id': has_parent(obj)})
                        else:
                            all_items.append({'id': obj.id, 'url': item.get_absolute_url(), 'title': obj.title, 'parent_id': has_parent(obj)})
                            
                    except Exception, err:
                        print err
    except Exception, err:
        print err
    #return a tuple of title and its items
    return (menu_title, all_items)
    
    
def get_menu_options(position_id):
    """
    Get full menu options as in settings based on given position ID.
    """
    try:
        available_menus = settings.AVAILABLE_MENUS
    except AttributeError:
        return
    else:
        for menu in available_menus:
            if menu['id'] == position_id:
                return menu
                break
    return

def get_menu_components(position_id):
    """
    Prepare menu component based on menu options in settings.
    """
    
    menu_options = get_menu_options(position_id)
    if not menu_options:
        return (None, None)
    
    list_type = menu_options.get('type', 'UL')
    list_class = menu_options.get('class', None)
    
    if list_class:
        lclass = list_class
    else:
        lclass = ''
    
    if list_type != 'UL':
        list_tag = 'ol'
    else:
        list_tag = 'ul'
        
    return (list_tag, lclass)
    
