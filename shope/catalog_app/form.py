from django import forms


class CartEditForm(forms.Form):
    product = forms.CharField(max_length=6)
    product_name = forms.CharField(max_length=250)
    image = forms.CharField(max_length=250)
    count = forms.CharField(max_length=6)
    amount = forms.CharField(max_length=50)
    seller = forms.CharField(max_length=6)

    class Meta:
        fields = ['product', 'product_name', 'image', 'count', 'amount', 'seller']
