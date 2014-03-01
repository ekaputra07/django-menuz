from django.core.urlresolvers import reverse
from django.conf import settings

from menuz.models import Menuz, MenuzItem
from menuz.registry import menuz
from menuz.registry import get_menuz_object_model


def get_menu_positions():
    """
    Get All menu positions
    """
    try:
        available_menus = settings.AVAILABLE_MENUS
    except Exception:
        return ((None, None))
    else:
        return ((menu['id'], menu['title']) for menu in available_menus)


def get_menu_by_position(position):
    """
    Return all menu items based on position ID.
    """
    menu_title = ''
    all_items = []
    #get all menu items

    def get_menu_parent(obj):
        if obj.parent:
            return obj.parent.id
        return 0

    try:
        menu = Menuz.objects.get(position__exact=position)
        menu_title = menu.title
        menu_items = menu.menuzitem_set.all()
        #get all menu data, and return title and links only

        for obj in menu_items:
            if obj.content_type == 'custom' or obj.content_type == 'innerlink':
                all_items.append({
                    'id': obj.id,
                    'url': obj.url,
                    'title': obj.title,
                    'parent_id': get_menu_parent(obj)})
            else:
                menu_model = get_menuz_object_model(obj.content_type)
                if menu_model:
                    try:
                        item = menu_model.objects.get(pk=obj.content_id)
                        all_items.append({'id': obj.id,
                                         'obj_id': item.pk,
                                         'url': item.get_absolute_url(),
                                         'title': obj.title,
                                         'parent_id': get_menu_parent(obj)})
                    except Exception as err:
                        pass
    except Exception as err:
        pass
    #return a tuple of title and its items
    return (menu_title, all_items)


def get_menu_options(position_id):
    """
    Get full menu options as in settings, based on given position ID.
    """
    try:
        available_menus = settings.AVAILABLE_MENUS
    except AttributeError:
        return
    else:
        for menu in available_menus:
            if menu['id'] == position_id:
                return menu
    return


def get_menu_components(position_id):
    """
    Prepare menu component based on menu options in settings.
    """

    menu_options = get_menu_options(position_id)
    if not menu_options:
        return (None, None)

    list_type = menu_options.get('type', 'UL')
    list_class = menu_options.get('class', '')
    before_link = menu_options.get('before_link', '')
    after_link = menu_options.get('after_link', '')

    if list_type != 'UL':
        list_tag = 'ol'
    else:
        list_tag = 'ul'

    return (list_tag, list_class, before_link, after_link)


def count_menu_children(menu_items, parent_id):
    """
    Count menu clhildren in current menu items based on parent menu ID
    """
    counter = 0
    for menu in menu_items:
        if menu['parent_id'] == parent_id:
            counter += 1
    return counter
