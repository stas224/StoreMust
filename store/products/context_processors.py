from products.models import Basket


def baskets(request):
    user = request.user
    return {'basket': Basket.objects.filter(user=user) if user.is_authenticated else []}