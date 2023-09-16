from django import forms


class FilterForm(forms.Form):

    class Meta:
        fields = ('product_name', 'min_price', 'max_price', 'product_in_stock', 'free_delivery')

    product_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название', 'autofocus': True}))
    min_price = forms.IntegerField(min_value=100)
    max_price = forms.IntegerField(max_value=15000)
    product_in_stock = forms.BooleanField()
    free_delivery = forms.BooleanField()
