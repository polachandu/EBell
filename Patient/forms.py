from django import forms

from Patient.models import Bell


class BellForm(forms.Form):
     
    message = forms.CharField(max_length=120)
    priority = forms.IntegerField()
    staff = forms.CharField(max_length=10)
    emergency = forms.CharField(max_length=5)
    room_number = forms.IntegerField()
    time = forms.TimeField()
