from django import forms
from store.models import Categorymodel, User,Productmodel



class Userregisterform(forms.ModelForm):

    class Meta:

        model=User

        fields=['username','first_name','last_name','email','password']


class Loginform(forms.Form):

    username=forms.CharField()
    
    password=forms.CharField()


class Categoryform(forms.ModelForm):

    class Meta:

        model=Categorymodel
        
        fields="__all__"


class Productform(forms.ModelForm):

    class Meta:

        model=Productmodel

        fields="__all__"


class Orderform(forms.Form):

    address=forms.Textarea(widgets={forms.TextInput(attrs={'class':'form-control'})})


