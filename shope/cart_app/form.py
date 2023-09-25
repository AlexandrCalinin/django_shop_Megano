from django import forms


class ChangeCountForm(forms.Form):
    product = forms.CharField(max_length=8)
    count = forms.CharField(max_length=8)
    seller = forms.CharField(max_length=8)

    class Meta:
        fields = ['product', 'count', 'seller']
