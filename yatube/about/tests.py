from django.test import TestCase, Client
from http import HTTPStatus


class StaticUrlTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_urls(self):
        urls = ['/about/author/', '/about/tech/']
        for url in urls:
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
