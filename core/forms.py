import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Item


PAYMENT_CHOICES = (
    ('M', 'Mpesa'),
)

COUNTIES = (
    ('Nairobi', 'Nairobi'),
    ('Kisumu', 'Kisumu'),
    ('Mombasa', 'Mombasa'),
    ('Nakuru', 'Nakuru'),
    ('Kericho', 'Kericho'),
)
TOWNS =(
        ('within_nairobi','-----------------WITHIN NAIROBI-----------------'),
        ('Embakasi','Embakasi'),
        ('Kibera','Kibera'),
        ('Langata','Langata'),

        ('within_kisumu','-----------------WITHIN KISUMU-----------------'),
        ('Nyakach','Nyakach'),
        ('Seme','Seme'),
        ('Awasi','Awasi'),

        ('within_mombasa','-----------------WITHIN MOMBASA---------------'),
        ('Mvita','Mvita'),
        ('Jomvu','Jomvu'),
        ('Kisauni','Kisauni'),

        ('within_nakuru','-----------------WITHIN NAKURU-----------------'),
        ('Njoro','Njoro'),
        ('Bahati','Bahati'),
        ('Molo','Molo'),
        ('Naivasha','Naivasha'),

        ('within_kericho','-----------------WITHIN KERICHO-----------------'),    
        ('Belgut','Belgut'),
        ('Bureti','Bureti'),
)
PICK_STATION = (
        ('within_em','-----------------WITHIN EMBAKASI-----------------'),
        ('Daima Spring Pick-up station near Pipeline AIC', 'Daima Spring Pick-up station near Pipeline AIC'),
        ('Fedha Estate Pick-up station opposite Ora Petrol Station', 'Fedha Estate Pick-up station opposite Ora Petrol Station'),

        ('within_kib','-----------------WITHIN KIBERA-----------------'),
        ('Kianda Pick-up station opposite Naivas Supermarket', 'Kianda Pick-up station opposite Naivas Supermarket'),
        ('Lindi Pick-up station along Lindi Road', 'Lindi Pick-up station along Lindi Road'),

        ('within_la','-----------------WITHIN LANGATA-----------------'),
        ('Bera Pick-up station near Karen International School', 'Bera Pick-up station near Karen International School'),
        ('Asyana.G Pick-up station along Ngong Road', 'Asyana.G Pick-up station along Ngong Road'),
        ('Karen Handy Pick-up station near Karen Mall', 'Karen Handy Pick-up station near Karen Mall'),

        ('within_ny','-----------------WITHIN NYAKACH-----------------'),
        ('Jogoo pick-up station at Katito Market', 'Jogoo pick-up station at Katito Market'),
        ('Edgers LG pick-up station at kolweny Market', 'Edgers LG pick-up station at kolweny Market'),

        ('within_se','-----------------WITHIN SEME-----------------'),
        ('Bodi pick-up station near Jengo Clinic', 'Bodi pick-up station near Jengo Clinic'),
        ('Elha pick-up station along Bondo Boad', 'Elha pick-up station along Bondo Boad'),

        ('within_aw','-----------------WITHIN AWASI-----------------'),
        ('Awasi center pick-up station near Awasi Junction', 'Awasi center pick-up station near Awasi Junction'),

        ('within_mv','-----------------WITHIN MVITA-----------------'),
        ('Mokupa pick-up station near Harvard Supermarket', 'Mokupa pick-up station near Harvard Supermarket'),
        ('Kibokoni pick-up station along Kibokoni Road', 'Kibokoni pick-up station along Kibokoni Road'),

        ('within_jo','-----------------WITHIN JOMVU-----------------'),
        ('Miritini pick-up station near Total Petrol Station', 'Miritini pick-up station near Total Petrol Station'),

        ('within_ki','-----------------WITHIN KISAUNI-----------------'),
        ('Mbwere pick-up station along Mbwere Road', 'Mbwere pick-up station along Mbwere Road'),
        ('Watamu pick-up station opposite Jamaa House', 'Watamu pick-up station opposite Jamaa House'),

        ('within_nj','-----------------WITHIN NJORO-----------------'),
        ('Shalimo pick-up station along Molo-Njoro Road', 'Shalimo pick-up station along Molo-Njoro Road'),
        ('Egerton pick-up station at Egerton Market', 'Egerton pick-up station at Egerton Market'),

        ('within_ba','-----------------WITHIN BAHATI-----------------'),
        ('Wendo pick-up station along Miriti Road', 'Wendo pick-up station along Miriti Road'),
        ('Githioro pick-up station near Boss Hardware', 'Githioro pick-up station near Boss Hardware'),

        ('within_mo','-----------------WITHIN MOLO-----------------'),
        ('Jamaa pick-up station opposite Ibra Hotel', 'Jamaa pick-up station opposite Ibra Hotel'),
        ('Turi Center pick-up station near Molo Fine Milk Shop', 'Turi Center pick-up station near Molo Fine Milk Shop'),

        ('within_na','-----------------WITHIN NAIVASHA-----------------'),
        ('Oserian pick-up station near Nairobi Women Hospital', 'Oserian pick-up station near Nairobi Women Hospital'),
        ('Karagita pick-up station opposite Karagita AIC', 'Karagita pick-up station opposite Karagita AIC'),

        ('within_be','-----------------WITHIN BELGUT-----------------'),
        ('Litein pick-up station along Kericho-Bomet Road', 'Litein pick-up station along Kericho-Bomet Road'),
        ('Kabianga pick-up station at Kabianga Market', 'Kabianga pick-up station at Kabianga Market'),

        ('within_bu','-----------------WITHIN BURETI-----------------'),
        ('Kipteleny pick-up station near UDA House', 'Kipteleny pick-up station near UDA House'),
        ('Sesur pick-up station opposite Sesur Police Station', 'Sesur pick-up station opposite Sesur Police Station'),
)

#user authentication for signup
class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Regex pattern to validate email structure
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format. Please enter a valid email address (e.g., example@domain.com).")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Validate password length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Validate password contains at least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Validate password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Validate password contains at least one digit
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")

        # Validate password contains at least one special character
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`' for char in password):
            raise ValidationError("Password must contain at least one special character (e.g., !@#$%^&*).")
        
        return password

#for login
class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class CheckoutForm(forms.Form):    
    county = forms.ChoiceField(choices=(('', 'Select Your County'),) + COUNTIES, widget=forms.Select(attrs={'class': 'form-control custom-select d-block w-100', 'id': 'id_county'}))
    billing_address = forms.ChoiceField(choices=(('', 'Select Town as per County'),) + TOWNS, widget=forms.Select(attrs={'class': 'form-control custom-select d-block w-100', 'id': 'id_town'}))
    pick_station = forms.ChoiceField(choices=(('', 'Select Station as per Town'),) + PICK_STATION, widget=forms.Select(attrs={'class': 'form-control custom-select d-block w-100', 'id': 'id_pick_station'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add zip','class': 'form-control'}))
    #same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)    
    
class PaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'2541xx or 2547xx'}))
    
class MpesaForm(forms.Form):
    phone_number = forms.CharField(max_length=15, required=True)
    amount = forms.DecimalField(required=True)
    account_reference = forms.CharField(max_length=100, required=True)
    transaction_desc = forms.CharField(max_length=100, required=True)
    callback_url = forms.URLField(required=True)

class PostForm(forms.ModelForm):
    class Meta:
        model = Item
        fields =['image_title', 'cover']

class RefundForm(forms.Form):
    reference_code = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':4})) 