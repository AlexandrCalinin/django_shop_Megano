from core.utils.add_product_to_cart import AddProductToCart


def cart_processor(request):
    amount, count = AddProductToCart().get_count_product_in_cart(user=request.user)

    return {'count': count, 'amount': amount}
