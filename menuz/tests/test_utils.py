from django.test import TestCase
from django.test.utils import override_settings
from django.db import models

from menuz.utils import (get_menu_positions, get_menu_components,
                         get_menu_options, count_menu_children)

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
        {
            'id': 'footer_menu',
            'title': 'Footer Menu',
            'type': 'OL',
            'class': None,
        },
    )
)
class TestMenuzUtils(TestCase):

    def test_get_menu_positions(self):

        pos = list(get_menu_positions())
        self.assertEqual(2, len(pos))
        self.assertEqual('top_menu', pos[0][0])
        self.assertEqual('Footer Menu', pos[1][1])

    def test_get_menu_options(self):

        opts = get_menu_options('top_menu')
        self.assertEqual('top_menu', opts['id'])
        self.assertEqual('UL', opts['type'])
        self.assertEqual('Top Menu', opts['title'])

    def test_get_menu_components(self):

        list_tag, list_class, before_link, after_link = get_menu_components('top_menu')
        self.assertEqual('ul', list_tag)
        self.assertEqual('someclass', list_class)
        self.assertEqual('BBB', before_link)
        self.assertEqual('AAA', after_link)

    def test_count_menu_children(self):
        menu_items_sample = [
            {'parent_id': 1},
            {'parent_id': 2},
            {'parent_id': 3},
            {'parent_id': 2},
            {'parent_id': 2},
            {'parent_id': 2},
        ]
        counter = count_menu_children(menu_items_sample, 2)
        self.assertEqual(4, counter)

