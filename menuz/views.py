from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template import RequestContext

from menuz.models import Menuz, MenuzItem
from menuz.forms import CustomMenuForm
from menuz.registry import get_menuz_object_model

@login_required
def add_menuz(request):
    if request.is_ajax():
        if request.method == 'POST':
            mtype = request.POST.get('mtype','')
            menu_id = request.POST.get('menu_id',0)
            menu = Menuz.objects.get(pk=menu_id)

            #if menu type custom
            if mtype == 'custom':
                customform = CustomMenuForm(request.POST)
                if customform.is_valid():

                    menuitem = MenuzItem()
                    menuitem.menu = menu
                    menuitem.content_type = mtype
                    menuitem.title = strip_tags(customform.cleaned_data['custom_title'])
                    menuitem.url = customform.cleaned_data['custom_url']
                    menuitem.save()
                    data = {
                        'id': menuitem.id,
                        'title': menuitem.title,
                        'url': menuitem.url,
                        'content_type': menuitem.content_type,
                        'content_id': menuitem.content_id
                    }
                    menu_data = [data]
                    return HttpResponse(simplejson.dumps({'status':'success', 'menu_data': menu_data}),
                                        content_type='application/javascript; charset=utf-8;')
                else:
                    fields = [field for field in customform.errors]
                    return HttpResponse(simplejson.dumps({'status':'failed', 'fields':fields}),
                                        content_type='application/javascript; charset=utf-8;')

            #if menu type Innerlink, similar to custom but different treatment
            elif mtype == 'innerlink':

                links = request.POST.getlist(mtype)

                if links and menu:
                    menu_data = []
                    for link in links:
                        link_split = link.split('$')

                        menuitem = MenuzItem()
                        menuitem.menu = menu
                        menuitem.content_type = mtype
                        menuitem.title = strip_tags(link_split[1])
                        menuitem.url = strip_tags(link_split[0])
                        menuitem.save()

                        data = {
                            'id': menuitem.id,
                            'title': menuitem.title,
                            'url': menuitem.url,
                            'content_type': menuitem.content_type,
                            'content_id': menuitem.content_id
                        }
                        menu_data.append(data)
                    return HttpResponse(simplejson.dumps({'status':'success', 'menu_data': menu_data}),
                                        content_type='application/javascript; charset=utf-8;')

            #if menu type Model Menu
            else:
                obj_ids = request.POST.getlist(mtype)
                model = get_menuz_object_model(mtype)

                if obj_ids and menu and model:
                    queryset = model.objects.filter(pk__in=obj_ids)
                    menu_data = []
                    for obj in queryset:

                        menuitem = MenuzItem()
                        menuitem.menu = menu
                        menuitem.content_type = mtype
                        menuitem.content_id = obj.pk
                        menuitem.title = obj.__unicode__()
                        menuitem.save()

                        data = {
                            'id': menuitem.id,
                            'title': menuitem.title,
                            'url': menuitem.url,
                            'content_type': menuitem.content_type,
                            'content_id': menuitem.content_id
                        }
                        menu_data.append(data)
                    return HttpResponse(simplejson.dumps({'status':'success', 'menu_data': menu_data}),
                                        content_type='application/javascript; charset=utf-8;')

            return HttpResponse(simplejson.dumps({'status':'failed'}),
                                    content_type='application/javascript; charset=utf-8;')


@login_required
def reorder_menuz(request):
    if request.is_ajax():
        if request.method == 'POST':
        
            menus = request.POST.get('order','')
            changed_item_id = request.POST.get('item_id', 0)
            changed_parent_id = request.POST.get('parent_id', None)
            
            if menus:
                try:
                    menu_ids = menus.split(',')
                    count = 1
                    #main loop to re-set menu order value
                    for m_id in menu_ids:
                        try:
                            menu = MenuzItem.objects.get(pk=m_id)
                            menu.order = count
                            
                            if m_id == changed_item_id:
                                menu.parent_id = changed_parent_id
                                
                            menu.save()
                            count += 1
                        except:
                            pass
                    return HttpResponse(simplejson.dumps({'status':'success'}),
                                        content_type='application/javascript; charset=utf-8;')
                except:
                    pass
            return HttpResponse(simplejson.dumps({'status':'Failed re-ordering menus!'}),
                                content_type='application/javascript; charset=utf-8;')
                                
@login_required
def delete_menuz(request):
    if request.is_ajax():
        item_id = request.POST.get('item_id',0)
        if item_id:
            try:
                menu_obj = MenuzItem.objects.get(pk=item_id)
                menu_obj.delete()
                return HttpResponse(simplejson.dumps({'status':'success'}),
                            content_type='application/javascript; charset=utf-8;')
            except MenuzItem.DoesNotExist:
                pass

        return HttpResponse(simplejson.dumps({'status':'failed'}),
                            content_type='application/javascript; charset=utf-8;')
                            
@login_required
def update_menuz(request):
    if request.is_ajax():
        if request.method == 'POST':
            mtype = request.POST.get('mtype', '')
            item_id = request.POST.get('item_id', 0)

            status = False
            #try to get menu item object
            item = None
            try:
                item = MenuzItem.objects.get(pk=item_id)
            except MenuzItem.DoesNotExist:
                pass

            #if menu item found
            if item:
                title = request.POST.get(mtype+'_title_'+item_id, '')
                #if menu type custom link
                #update title and Url
                if mtype == 'custom':
                    url = request.POST.get(mtype+'_url_'+item_id, '')
                    if title and url:
                        item.title = strip_tags(title)
                        item.url = strip_tags(url)
                        item.save()
                        status = True
                else:
                    if title:
                        item.title = strip_tags(title)
                        item.save()
                        status = True
            if status:
                return HttpResponse(simplejson.dumps({'status':'success', 'new_title': item.title}),
                                content_type='application/javascript; charset=utf-8;')
            else:
                return HttpResponse(simplejson.dumps({'status':'failed'}),
                                content_type='application/javascript; charset=utf-8;')


# Hierarchy menu rendering for django-menuz admin panel
def render_children(parent, menu_items, request):
    """
    rendering the childrens menu recursively.
    """
    
    childs = []
    output = []
    
    for menu in menu_items:
        if menu.parent == parent:
            childs.append(menu)

    if childs:
        output.append('<ol>')
        for child in childs:
            output.append('<li rel="%s">' % child.id)
            output.append(render_to_string('admin/menuz/menuz/menu_item.html', {'item': child}, context_instance=RequestContext(request)))
            output.append(render_children(child, menu_items, request))
            output.append('</li>')
        output.append('</ol>')
    
    return ''.join(output)
    

@login_required
def reload_menuz(request, container_id):

    if request.is_ajax() and  request.method == 'GET':
        
        menu_items = MenuzItem.objects.filter(menu__id=container_id).order_by('order')
        output = []
        
        if menu_items:
            output.append('<ol class="sortable">')
            for menu in menu_items:
                if not menu.parent:
                    output.append('<li rel="%s">' % menu.id)
                    output.append(render_to_string('admin/menuz/menuz/menu_item.html', {'item': menu}, context_instance=RequestContext(request)))
                    output.append(render_children(menu, menu_items, request))
                    output.append('</li>')
            output.append('</ol>')
        
        return HttpResponse(u''.join(output))
    else:
        raise Http404
