from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'StoreMust'


class ProductsListView(TitleMixin, ListView):
    template_name = 'products/products.html'
    model = Product
    paginate_by = 3
    title = 'StoreMust - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_name = self.kwargs.get('category_name')
        return queryset.filter(category__name=category_name) if category_name else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket_update_quantity = basket.first()
        basket_update_quantity.quantity += 1
        basket_update_quantity.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
