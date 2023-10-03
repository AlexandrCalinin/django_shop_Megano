from core.utils.add_product_to_cart import AddProductToCart


def cart_processor(request):

    if request.user.is_authenticated:

        amount, count = AddProductToCart().get_count_product_in_cart(user=request.user)
        return {'amount': amount, 'count': count}

    else:

        amount, count = AddProductToCart().get_count_product_for_anonymous_user(request)
        return {'amount': amount, 'count': count}
