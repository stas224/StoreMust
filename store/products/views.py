from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Product, ProductCategory, Basket

from users.models import User


def index(request):
    context = {
        'title': 'StoreMust',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'StoreMust - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context)


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
