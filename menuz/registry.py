"""
This section take its concept from django admin site.
with similar aproach and implementation.

Implementation:
in project root urls.py add folowing code:


from menuz import registry
registry.autodiscover()

This will try to import all file in apps that named menu.py.
"""

class MenuzRegistry(object):

    def __init__(self):
        self.registry = []

    def register(self, model, custom_source=None):
        if model:
            if model in self.registry:
                pass
            else:
                meta = {
                    'type' : model.__name__.lower(),
                    'model': model,
                    'custom_source': custom_source
                }
                self.registry.append(meta)

menuz = MenuzRegistry()

def autodiscover():

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module

    for app in settings.INSTALLED_APPS:
        try:
            before_import_registry = copy.copy(menuz.registry)
            import_module('%s.menu' % app)
        except:
            menuz.registry = before_import_registry

def get_menuz_object_model(content_type):
    for menu in menuz.registry:
        if menu['type'] == content_type:
            return menu['model']
            break
    return False
