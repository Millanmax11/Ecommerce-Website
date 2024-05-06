from django import forms
from .models import Item


PAYMENT_CHOICES = (
    ('M', 'Mpesa'),
)

COUNTIES = (
    ('nairobi', 'Nairobi'),
    ('kisumu', 'Kisumu'),
    ('mombasa', 'Mombasa'),
    ('nakuru', 'Nakuru'),
    ('kericho', 'Kericho'),
)
TOWNS =(
        ('within_nairobi','-----------------WITHIN NAIROBI-----------------'),
        ('embakasi','Embakasi'),
        ('kibera','Kibera'),
        ('langata','Langata'),

        ('within_kisumu','-----------------WITHIN KISUMU-----------------'),
        ('nyakach','Nyakach'),
        ('seme','Seme'),
        ('awasi','Awasi'),

        ('within_mombasa','-----------------WITHIN MOMBASA---------------'),
        ('mvita','Mvita'),
        ('jomvu','Jomvu'),
        ('kisauni','Kisauni'),

        ('within_nakuru','-----------------WITHIN NAKURU-----------------'),
        ('njoro','Njoro'),
        ('bahati','Bahati'),
        ('molo','Molo'),
        ('naivasha','Naivasha'),

        ('within_kericho','-----------------WITHIN KERICHO-----------------'),    
        ('belgut','Belgut'),
        ('bureti','Bureti'),
)
PICK_STATION = (
        ('within_em','-----------------WITHIN EMBAKASI-----------------'),
        ('Daima_Spring_Pick-up', 'Daima Spring Pick-up station near Pipeline AIC'),
        ('Fedha_Estate_Pick-upn', 'Fedha Estate Pick-up station opposite Ora Petrol Station'),

        ('within_kib','-----------------WITHIN KIBERA-----------------'),
        ('Kianda_Pick-up', 'Kianda Pick-up station opposite Naivas Supermarket'),
        ('Lindi_Pick-up', 'Lindi Pick-up station along Lindi Road'),

        ('within_la','-----------------WITHIN LANGATA-----------------'),
        ('Bera_Pick-up', 'Bera Pick-up station near Karen International School'),
        ('Asyana.G_Pick-up', 'Asyana.G Pick-up station along Ngong Road'),
        ('Karen_Handy_Pick-up', 'Karen Handy Pick-up station near Karen Mall'),

        ('within_ny','-----------------WITHIN NYAKACH-----------------'),
        ('Jogoo_pick-up', 'Jogoo pick-up station at Katito Market'),
        ('Edgers_LG_pick-up', 'Edgers LG pick-up station at kolweny Market'),

        ('within_se','-----------------WITHIN SEME-----------------'),
        ('Bodi_pick-up', 'Bodi pick-up station near Jengo Clinic'),
        ('Elha_pick-up', 'Elha pick-up station along Bondo Boad'),

        ('within_aw','-----------------WITHIN AWASI-----------------'),
        ('Awasi_center_pick-up', 'Awasi center pick-up station near Awasi Junction'),

        ('within_mv','-----------------WITHIN MVITA-----------------'),
        ('Mokupa_pick-up', 'Mokupa pick-up station near Harvard Supermarket'),
        ('Kibokoni_pick-up', 'Kibokoni pick-up station along Kibokoni Road'),

        ('within_jo','-----------------WITHIN JOMVU-----------------'),
        ('Miritini_pick-up', 'Miritini pick-up station near Total Petrol Station'),

        ('within_ki','-----------------WITHIN KISAUNI-----------------'),
        ('Mbwere_pick-up', 'Mbwere pick-up station along Mbwere Road'),
        ('Watamu_pick-up', 'Watamu pick-up station opposite Jamaa House'),

        ('within_nj','-----------------WITHIN NJORO-----------------'),
        ('Shalimo_pick-up', 'Shalimo pick-up station along Molo-Njoro Road'),
        ('Egerton_pick-up', 'Egerton pick-up station at Egerton Market'),

        ('within_ba','-----------------WITHIN BAHATI-----------------'),
        ('Wendo_pick-up', 'Wendo pick-up station along Miriti Road'),
        ('Githioro_pick-up', 'Githioro pick-up station near Boss Hardware'),

        ('within_mo','-----------------WITHIN MOLO-----------------'),
        ('Jamaa_pick-up', 'Jamaa pick-up station opposite Ibra Hotel'),
        ('Turi Center_pick-up', 'Turi Center pick-up station near Molo Fine Milk Shop'),

        ('within_na','-----------------WITHIN NAIVASHA-----------------'),
        ('Oserian_pick-up', 'Oserian pick-up station near Nairobi Women Hospital'),
        ('Karagita_pick-up', 'Karagita pick-up station opposite Karagita AIC'),

        ('within_be','-----------------WITHIN BELGUT-----------------'),
        ('Litein_pick-up', 'Litein pick-up station along Kericho-Bomet Road'),
        ('Kabianga_pick-up', 'Kabianga pick-up station at Kabianga Market'),

        ('within_bu','-----------------WITHIN BURETI-----------------'),
        ('Kipteleny_pick-up', 'Kipteleny pick-up station near UDA House'),
        ('Sesur_pick-up', 'Sesur pick-up station opposite Sesur Police Station'),
)
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