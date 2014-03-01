from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

from menuz.models import Menuz, MenuzItem
from menuz.tests import ModelSample


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='admin', is_active=True)
        self.user.set_password('admin')
        self.user.save()

        self.client.login(username='admin', password='admin')

        self.menu = Menuz.objects.create(title='Top menu', position='top_menu')

    def test_add_menu(self):
        url = reverse('add_menuz')

        # Should return 404, not Ajax
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)

        # Add custom menu
        resp = self.client.post(url, {'mtype': 'custom',
                                      'menu_id': self.menu.pk,
                                      'custom_title': 'Hello menu',
                                      'custom_url': 'http://google.com/', },
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('success' in resp.content)

        # Add innerlink menu
        resp = self.client.post(url, {'mtype': 'innerlink',
                                      'menu_id': self.menu.pk,
                                      'innerlink': '/some_page/$Some page', },
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('success' in resp.content)

        # Add Model menu
        model_sample = ModelSample(title='Some title')
        model_sample.save()

        resp = self.client.post(url, {'mtype': ModelSample.__name__.lower(),
                                      'menu_id': self.menu.pk,
                                       ModelSample.__name__.lower(): model_sample.pk, },
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('success' in resp.content)

    def test_reload_menu(self):
        url = reverse('reload_menuz', kwargs={'container_id': self.menu.pk, })

        # Should return 404, not Ajax
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

        # Should return 200, Ajax call
        resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
