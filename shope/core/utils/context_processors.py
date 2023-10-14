from catalog_app.models import Category
from core.utils.add_product_to_cart import AddProductToCart


def cart_processor(request):

    if request.user.is_authenticated:

        amount, count = AddProductToCart().get_count_product_in_cart(user=request.user)
        return {'amount': amount, 'count': count}

    else:

        amount, count = AddProductToCart().get_count_product_for_anonymous_user(request)
        return {'amount': amount, 'count': count}


def get_category_list(request):
    cat_lst = Category.objects.all().prefetch_related('characteristictype_set')
    return {'category_list': cat_lst}
