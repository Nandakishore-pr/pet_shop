from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from account.models import User,Profile,Address



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
        
            raise ValidationError(_('Last name should only contain letters and/or numbers.'))
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

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'postal_code', 'country', 'is_default']  # Add or remove fields as needed