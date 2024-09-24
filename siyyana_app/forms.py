from django import forms
from accounts.models import CustomUser
from siyyana_app.models import *





class ServicesAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control','required':True}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control', 'required': True}),
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
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control','required':True}),
            'service': forms.Select(attrs={'class': 'form-control','required':True}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(SubServicesAddForm, self).__init__(*args, **kwargs)

        # Make the img field not required during editing
        if self.instance.pk:
            self.fields['logo'].required = False
            self.fields['logo'].widget.attrs.pop('required', None)


class TopServicesAddForm(forms.ModelForm):
    class Meta:
        model = TopCategory
        fields = '__all__'

        widgets = {

            'Category': forms.Select(attrs={'class': 'form-control','required':True}),
        }


class TopSubServicesAddForm(forms.ModelForm):
    class Meta:
        model = TopSubCategory
        fields = '__all__'

        widgets = {

            'SubCategory': forms.Select(attrs={'class': 'form-control','required':True}),
        }




class CountryAddForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'flag' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
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




class EmployeeViewForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'name', 'mobile_number', 'whatsapp_number', 'profile_picture', 'about', 'category', 
            'subcategory', 'charge', 'date_of_birth', 'approval_status', 
            'country', 'state', 'district', 'prefered_work_location', 'id_card_type', 'id_card_number', 'id_card'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'disabled': True}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number', 'disabled': True}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp Number', 'disabled': True}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'disabled': True}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself', 'rows': 5, 'disabled': True}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control', 'disabled': True}),
            'subcategory': forms.SelectMultiple(attrs={'class': 'form-control', 'disabled': True}),
            'charge': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'disabled': True}),
            'approval_status': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'country': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'state': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'district': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'prefered_work_location': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'id_card_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Card Type', 'disabled': True}),
            'id_card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Card Number', 'disabled': True}),
            'id_card': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'disabled': True}),
        }




class OnboardingAddForm(forms.ModelForm):
    class Meta:
        model = Onbaording
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': True}),

        }



