from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from products.models import Product, ProductCategory


class TestIndexView(TestCase):

    def test_index(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'StoreMust')
        self.assertTemplateUsed(response, 'products/index.html')


class TestProductsListView(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'StoreMust - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)

        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products[:3])
        )

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_name': category.name})
        response = self.client.get(path)

        self._common_test(response)

        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category__name=category.name))
        )
