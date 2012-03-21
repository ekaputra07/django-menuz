DJANGO MENUZ
============

Django Menuz is another menu app for Django.

It mainly inspired by how easy menu creation ini WordPress. Django Menuz provides
template tags to call menu in specified location.

With it's drag and drop features, now its easy to assign menu items for specified location in template drag and drop it if you want to re-order the menu item position.

INSTALLATION AND USAGE:
-----------------------
Once you install it via setup.py, easy_install or pip.

* add **menuz** into your **INSTALLED_APPS** Django settings.py file.

* add codes below into your project **urls.py** :

::

    from menuz import registry
    registry.autodiscover()

* Also add url config below into projects urls configuration.

::

    url(r'', include('menuz.urls')),

* Register all available menu positions in project **settings.py** by adding **AVAILABLE_MENUS** parameter. example:

::

    #Available menus on site
    AVAILABLE_MENUS = (
        ('top_menu', u'Main top menu'),
        ('side_menu', u'Menu at sidebar'),
        ('position_id_must_be_unique', u'Position title goes here'),
        ...
        ...
        etc.
    )

* If you have few fix/static url into your application and want to include so it's will be selectable as a menu items, add **AVAILABLE_INNERLINKS** in your project **settings.py**.

::

    AVAILABLE_INNERLINKS = (
        ('/this_page/', 'This Page'),
        ('/that_page/', 'That Page'),
        ('/categories/', 'Categories Page'),
        ('/collections/', 'Collections Page'),
        ...
        ...
        etc.
    )

* Above links must inbound link, not links to other sites(outbound link).
* For Outbound link menu, use Custom link in menu creation admin page.

* To create a menu based on Django model items, simply create **menu.py** in application directory, this is in the same level as application urls.py and register our model as following example (file: menu.py).

::

    # file: menu.py
    from menuz.registry import menuz
    from catalog.models import Product

    menuz.register(Product)

* Or if you want to do some filtering before registering it into menuz do as follows (file: menu.py).

::

    from menuz.registry import menuz
    from catalog.models import Product

    def active_product():
        return Product.objects.filter(active=True)

    menuz.register(Product, custom_source=active_product)

We registering extra callback that will be called when menuz will display selectable menu items in admin area,
that way, the menu item selector will not display all available products, but will display active products only.

IMPORTANT:
----------
To make Model menu items links correctly to its url, your model must utilize **get_absolute_url()** function. Because this is the only standard way to retrieve object urls, at least for django-menuz.

example:

::

    from django.db.models import permalink

    @permalink
    get_absolute_url():
        return ('some_page', None, {'slug': self.slug})


CALLING MENU ITEMS IN TEMPLATE
------------------------------

**example calling menu items as template context**::

    {% load menuz_tags %}
    {% get_menu top_menu as tmenu %}

    <h2>{{tmenu_title}}</h2>
    <ul>
        {% for item in tmenu %}
        <li><a href="{{item.url}}">{{item.title}}</a></li>
        {% endfor %}
    </ul>

**example calling menu items as html list**::

    {% load menuz_tags %}
    <ul>
        {% list_menu top_menu %}
    </ul>

TODO:
-----
1. Add support for hierarchical menu creation.
2. Add filter in model menu selector, so it's will be easier to find record to use as menu item.

