from django.core.urlresolvers import reverse
from menuz.models import Menuz, MenuzItem
from menuz.registry import menuz
from menuz.registry import get_menuz_object_model


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
    try:
        menu = Menuz.objects.get(position__exact=position)
        menu_title = menu.title
        menu_contents = menu.menuzitem_set.all()
        #get all menu data, and return title and links only 
        
        for obj in menu_contents:
            if obj.content_type == 'custom' or obj.content_type == 'innerlink':
                all_items.append({'url': obj.url, 'title': obj.title})
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
                                all_items.append({'url': reverse('index'), 'title': obj.title})
                            else:
                                all_items.append({'url': item.get_absolute_url(), 'title': obj.title})
                        else:
                            all_items.append({'url': item.get_absolute_url(), 'title': obj.title})
                            
                    except Exception, err:
                        print err
    except Exception, err:
        print err
    #return a tuple of title and its items
    return (menu_title, all_items)

