from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.template import Template, RequestContext, TemplateSyntaxError
from django.db import models

from menuz.models import Menuz, MenuzItem
from menuz.tests import ModelSample

@override_settings(
    AVAILABLE_MENUS = (
        {
            'id': 'top_menu',
            'title': 'Top Menu',
            'type': 'UL',
            'class': 'someclass',
            'before_link': 'BBB',
            'after_link': 'AAA',
        },
    ),

    AVAILABLE_INNERLINKS = (
        ('/this_page/', 'This Page'),
        ('/that_page/', 'That Page'),
        ('/categories/', 'Categories Page'),
        ('/collections/', 'Collections Page'),
    )
)
class TestTemplateTags(TestCase):

    def setUp(self):
        # Create the menu
        menu = Menuz.objects.create(title='Top menu', position='top_menu')

        # Add some item to menu
        # 1. add custom menu
        menuCustom = MenuzItem()
        menuCustom.menu = menu
        menuCustom.content_type = 'custom'
        menuCustom.title = 'Menu Custom'
        menuCustom.url = 'http://google.com'
        menuCustom.save()

        # 2. add innerlink menu
        menuInnerlink = MenuzItem()
        menuInnerlink.menu = menu
        menuInnerlink.content_type = 'innerlink'
        menuInnerlink.title = 'Menu innerlink'
        menuInnerlink.url = '/some_page/'
        menuInnerlink.save()

        request_factory = RequestFactory()
        self.request = request_factory.get('/this_page/')
        self.context_instance = RequestContext(self.request)

    def test_list_menu_tag(self):
        render = lambda t: Template(t).render(self.context_instance)

        # Should failed, incorrect usage.
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load menuz_tags %}{% list_menu %}")
        self.assertRaises(ValueError, render,
                          "{% load menuz_tags %}{% list_menu top_menu %}")

        out = Template(
            "{% load menuz_tags %}"
            "{% list_menu 'top_menu' %}"
        ).render(self.context_instance)
        self.assertTrue('<ul' in out)
        self.assertTrue('<li' in out)
        self.assertTrue('Menu Custom' in out)
        self.assertTrue('Menu innerlink' in out)
        self.assertTrue('someclass' in out)
        self.assertTrue('>AAA' in out)
        self.assertTrue('BBB<a' in out)

    def test_get_menu_tag(self):
        render = lambda t: Template(t).render(self.context_instance)

        # Should failed, incorrect usage.
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load menuz_tags %}{% get_menu %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load menuz_tags %}{% get_menu top_menu %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load menuz_tags %}{% get_menu top_menu as %}")

        out = Template(
            "{% load menuz_tags %}"
            "{% get_menu top_menu as tmenu %}"
            "{{ tmenu_title }}"
            "{% for menu in tmenu %}"
            "{{menu.title}} {{menu.url}}"
            "{% endfor %}"
        ).render(self.context_instance)
        self.assertTrue('Top menu' in out)
        self.assertTrue('http://google.com' in out)
        self.assertTrue('/some_page/' in out)
