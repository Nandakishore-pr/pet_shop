from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from account.models import User,Profile,Address
import re


User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "First Name"}),
                                 required=True, help_text='Required. 30 characters or fewer.')
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
                                required=True, help_text='Required. 30 characters or fewer.')
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"placeholder": "Email"}), required=True,
                             help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
                                required=True, help_text='Required. 30 characters or fewer.')
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
                                required=True, help_text='Required. 30 characters or fewer.')
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Username"}), required=True,
                               help_text='Required. 30 characters or fewer.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1','password2']
        labels = {'email': 'Email'}

    # def clean(self):
    #     cleaned_data = super(User,self).clean()
    #     password1 = cleaned_data.get(password1)
    #     password2 = cleaned_data.get(password2)

    #     if password1 != password2:
    #         raise forms.ValidationError("password doesn't match")

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        # Check if the first name contains only letters
        if not first_name.isalpha():
            raise ValidationError(_('First name should only contain letters.'))

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError(_('Last name should only contain letters '))
        return last_name
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isalpha():
            raise ValidationError(_('Last name should only contain letters'))
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email address")
        return email



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'phone']  # Add or remove fields as needed

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name:
            if not full_name.replace(' ', '').isalpha():
                raise forms.ValidationError("Full name should only contain alphabetic characters.")
        return full_name
            
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio:
            if not bio.replace(' ', '').isalpha():
                raise ValidationError("Bio should only contain letters.") 
        return bio

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            pattern = r'^\d{10}$'
            if not re.match(pattern, phone):
                raise forms.ValidationError("Phone number must contain exactly 10 digits and no letters.")
        return phone

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'postal_code', 'country', 'is_default']  # Add or remove fields as needed


    def clean_street_address(self):
        street_address = self.cleaned_data.get('street_address')
        if street_address:
            if not street_address.replace(' ', '').isalpha():
                raise ValidationError("street address should only contain letters.") 
        return street_address
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city:
            if not city.replace(' ', '').isalpha():
                raise ValidationError("city name should only contain letters.") 
        return city
    
    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state:
            if not state.replace(' ', '').isalpha():
                raise ValidationError("state name should only contain letters.") 
        return state
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country:
            if not country.replace(' ', '').isalpha():
                raise ValidationError("state name should only contain letters.") 
        return country
    
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code:
            pattern = r'^\d{6}$'
            if not re.match(pattern, postal_code):
                raise forms.ValidationError("postal code must contain exactly 6 digits and no letters.")
        return postal_code