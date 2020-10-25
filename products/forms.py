from django import forms
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError


class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(51)])
    message = forms.CharField(required=False)
    instructions = forms.CharField(required=False)


class CheckoutForm(forms.Form):
    fullname = forms.CharField(required=False)
    delivery_date = forms.DateField(widget=forms.SelectDateWidget)
    address = forms.CharField(widget=forms.Textarea)

    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message="enter valid phone number eg: 9876543210")
    phone_number = forms.CharField(validators=[phone_regex])
    lists = (('kasaragod', 'kasaragod'),
             ('kumbala', 'kumbala'),
             ('eriyal', 'eriyal'),
             ('chowki', 'chowki'),)

    location = forms.ChoiceField(widget=forms.Select, choices=lists)

    def clean_delivery_date(self):
        data = self.cleaned_data['delivery_date']
        if data < datetime.date.today() + datetime.timedelta(days=1):
            raise forms.ValidationError("The date cannot be in the past!")
        return data
