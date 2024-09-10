from django import forms
from siyyana_app.models import *





class ServicesAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control','required':True}),
        }

    def __init__(self, *args, **kwargs):
        super(ServicesAddForm, self).__init__(*args, **kwargs)

        # Make the img field not required during editing
        if self.instance.pk:
            self.fields['logo'].required = False
            self.fields['logo'].widget.attrs.pop('required', None)



class SubServicesAddForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'service': forms.Select(attrs={'class': 'form-control','required':True}),
        }


class TopServicesAddForm(forms.ModelForm):
    class Meta:
        model = TopCategory
        fields = '__all__'

        widgets = {

            'Category': forms.Select(attrs={'class': 'form-control','required':True}),
        }


class CountryAddForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
        }



class StateAddForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'

        widgets = {
            'country': forms.Select(attrs={'class': 'form-control','required':True}),
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
        }




class DistrictAddForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'

        widgets = {
            'state': forms.Select(attrs={'class': 'form-control','required':True}),
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),

        }


