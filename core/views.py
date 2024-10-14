
from django import forms
import json
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomSignupForm  # Import the custom form
from .forms import CustomLoginForm
from datetime import datetime, timedelta
import base64
import random
import string
from itertools import chain
from django.db.models import Q

#----MPESA MODULES
#from access_tokens import tokens, scope
from django_daraja.mpesa.core import MpesaClient
import requests

#form module import
from .forms import CheckoutForm, PaymentForm, PostForm, RefundForm
from .models import Item, OrderItem, Order, Address, Transaction, Checkout, Refund, TrackOrder

# Create your views here.
def create_ref_code():
   return ''.join(random.choices( string.digits, k=14))

def create_track_number():
   return ''.join(random.choices( string.ascii_uppercase +string.digits, k=14))

def account_login(request):
  return render(request, "/account/login.html")

#Login
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are successfully logged in.")

                # If the user selected "Remember Me", set the session timeout to a longer duration (e.g., 1 week).
                if remember_me:
                    request.session.set_expiry(604800)  # Session will expire in 1 week (7 days)
                else:
                    request.session.set_expiry(0)  # Session expires when the browser is closed (default behavior)
                
                return redirect('core:homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            # Form is not valid, errors will be displayed
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomLoginForm()

    return render(request, 'account/login.html', {'form': form})

# Signup    
def custom_signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        
        if form.is_valid():  # If form passes all validation checks
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Create the user
            User.objects.create_user(username=username, email=email, password=password)

            messages.success(request, "Your account has been created successfully. You can now log in.")
            return redirect('account_login')  # Redirect to login page after signup
        else:
            # If the form is not valid, render the page again with the form errors
            return render(request, 'account/signup.html', {'form': form})
    else:
        form = CustomSignupForm()  # Show an empty form for GET request
        return render(request, 'account/signup.html', {'form': form})



class HomeView(ListView):
  model  =  Item
  template_name = "homepage.html"

class ItemDetailView(DetailView):
  model = Item
  template_name = "products.html"

def about(request):
  return render(request, "about.html")

def contact(request):
  return render(request, "contact.html")

def cart(request):
  return render(request, "cart.html")

def blog(request):
  return render(request, "blog.html")

#uploading an image to admin panel
def upload_image(request):
   if request.method =='POST':
      form = PostForm(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('core:homepage')
      else:
         form = PostForm()
      return render(request, 'upload.html', {'form':form})
#filter category
def category_view(request, category):
    if category == 'all':
        object_list = Item.objects.all()
    else:
        object_list = Item.objects.filter(category=category)
    return render(request, 'homepage.html', {'object_list': object_list})      

#action takes place in products
@login_required
def add_to_cart(request, slug):
  item = get_object_or_404(Item, slug=slug) 
  order_item, created = OrderItem.objects.get_or_create(
    item=item,
    user=request.user,
    ordered=False)
  order_qs = Order.objects.filter(user=request.user, ordered=False)
  if order_qs.exists():
    order=order_qs[0]

    #check if the order item is in the order
    if order.items.filter(item__slug=item.slug).exists():
      order_item.quantity += 1
      order_item.save()
      messages.info(request, "This item quantity was updated.")
      return redirect("core:product" , slug=slug)
    else:
      order.items.add(order_item)
      messages.info(request, "This item was added to your cart")
      return redirect("core:product", slug=slug)
  else:
    ordered_date = timezone.now()
    order = Order.objects.create(user=request.user, ordered_date=ordered_date)
    order.items.add(order_item)
    messages.info(request, "This item was added to your cart")
    return redirect("core:product", slug=slug)
  
  
# delete in the products---------action takes place in products
@login_required
def remove_from_cart(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order_qs = Order.objects.filter(user=request.user, ordered=False)

  if order_qs.exists():
    order = order_qs[0]   
    #check if the order item is in the order
    if order.items.filter(item__slug=item.slug).exists():
      order_item= OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
      )[0]
      order.items.remove(order_item)
      order_item.delete()
      messages.info(request, " This item was removed from your cart. ")
      return redirect( "core:product", slug=slug)
    else:
      messages.info(request, "This item was not in your cart. ")
      return redirect("core:product" , slug=slug)
  else:
    messages.info(request, "You do not have an active order. ")
    return redirect( "core:product",slug=slug)
  


  #delete in the cart--------- action takes place in cart
@login_required
def remove_single_from_cart(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order_qs = Order.objects.filter(user=request.user, ordered=False)

  if order_qs.exists():
    order = order_qs[0]   
    #check if the order item is in the order
    if order.items.filter(item__slug=item.slug).exists():
      order_item= OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
      )[0]
      order.items.remove(order_item)
      order_item.delete()
      messages.info(request, " This item was removed from your cart. ")
      return redirect( "core:order_summary")
    else:
      messages.info(request, "This item was not in your cart. ")
      return redirect("core:product",slug=slug)
  else:
    messages.info(request, "You do not have an active order. ")
    return redirect( "core:product",slug=slug)


#action takes place in cart
@login_required
def add_single_item_to_cart(request, slug):
  item = get_object_or_404(Item, slug=slug) 
  order_item, created = OrderItem.objects.get_or_create(
    item=item,
    user=request.user,
    ordered=False)
  order_qs = Order.objects.filter(user=request.user, ordered=False)
  if order_qs.exists():
    order=order_qs[0]

    #check if the order item is in the order
    if order.items.filter(item__slug=item.slug).exists():
      order_item.quantity += 1
      order_item.save()
      messages.info(request, "This item quantity was updated.")
      return redirect("core:order_summary")
    else:
      order.items.add(order_item)
      messages.info(request, "This item was added to your cart")
      return redirect("core:order_summary")
  else:
    ordered_date = timezone.now()
    order = Order.objects.create(user=request.user, ordered_date=ordered_date)
    order.items.add(order_item)
    messages.info(request, "This item was added to your cart")
    return redirect("core:order_summry")


# action takes place in cart
@login_required
def remove_single_item_from_cart(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order_qs = Order.objects.filter(user=request.user, ordered=False)

  if order_qs.exists():
    order = order_qs[0]   
    #check if the order item is in the order
    if order.items.filter(item__slug=item.slug).exists():
      order_item= OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
      )[0]
      if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
      else:
         order.items.remove(order_item)
      messages.info(request, "This item was updated")
      return redirect( "core:order_summary")
    else:
      messages.info(request, "This item was not in your cart. ")
      return redirect("core:product",slug=slug)
  else:
    messages.info(request, "You do not have an active order. ")
    return redirect( "core:product",slug=slug)
  

class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
           order = Order.objects.get(user=self.request.user, ordered=False)
           context = {
              'object': order
           }
           return render(self.request, 'cart.html', context)        
        except ObjectDoesNotExist:  
            messages.error(self.request, "You do not have active order")      
            return redirect("/")

def is_valid_form(values):
    valid = True
    for field in values:
        if field =='':
            valid = False
    return valid
      

#Checkout views
class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        #order        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'object': order
            }
            shipping_address_qs = Address.objects.filter(
               user=self.request.user,
               address_type='S',
               default=True
            )
            if shipping_address_qs.exists():
               context.update({'default_shipping_address': shipping_address_qs[0]})

            return render(self.request, 'checkout.html', context)        
        except ObjectDoesNotExist:  
            messages.error(self.request, "You do not have an active order")      
            return redirect("/")     
    def post(self,payment_option, *args, **kwargs):      
        form = CheckoutForm(self.request.POST or None)
        try:       
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                        )
                    if address_qs.exists():
                        shipping_address=address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping address exist")
                        return redirect('core:checkout')
                else:
                    print("User is entering new shipping address")
                    county = form.cleaned_data.get('county')               
                    billing_address = form.cleaned_data.get('billing_address')
                    pick_station = form.cleaned_data.get('pick_station')
                    zip = form.cleaned_data.get('zip')                  

                    if is_valid_form([county, billing_address, pick_station, zip]):
                        #save billing address in Address model
                        shipping_address = Address(
                        user = self.request.user,
                        county = county,
                        town_address = billing_address,
                        pick_station = pick_station,                    
                        zip = zip,    
                        address_type ='S'     
                        )
                        shipping_address.save() 

                        #save checkout in checkout model
                        checkouts = Checkout(
                        user = self.request.user,
                        county = county,
                        town_address = billing_address,
                        pick_station = pick_station,
                        zip =zip,
                        )
                        checkouts.save()
                        order.checkouts = checkouts
                        order.save()

                        #set both billing and checkout in order field inside Order model
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address")
                        return redirect("core:checkout")
                payment_option = form.cleaned_data.get('payment_option')                             
                messages.success(self.request, "Successful checkout")
                return redirect('core:payment', payment_option=payment_option)
            else:
                messages.warning(self.request, "Failed checkout")
                return redirect('core:checkout')               
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have active order")      
            return redirect("core:order_summary")
        

#####---pay                    #####-------MPESA-------------#####
class PaymentView(LoginRequiredMixin, View):
    def get(self,request, *args, **kwargs):
        #order
        form = PaymentForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'form': form,
                'object': order
            }
            return render(self.request, 'payment.html', context)        
        except ObjectDoesNotExist:  
            messages.error(self.request, "You do not have an active order")      
            return redirect("/")     
    def post(self,request, *args, **kwargs):                
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST or None)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            #test
            cl = MpesaClient()    
            # Generate the access token
            access_token = cl.access_token()            
            # Print the access token for testing
            #print("this is the token",access_token)            
            if access_token:
                amount = order.get_total()
                phone_number = phone_number
                process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                callback_url = 'https://api.darajambili.com/express-payment'
                passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
                business_short_code = '174379'
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
                party_a = phone_number
                party_b = phone_number
                account_reference = 'LIVING GARDENS'
                transaction_desc = 'millan straggle'
                stk_push_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
                
                stk_push_payload = {
                    'BusinessShortCode': business_short_code,
                    'Password': password,
                    'Timestamp': timestamp,
                    'TransactionType': 'CustomerPayBillOnline',
                    'Amount': amount,
                    'PartyA': party_a,
                    'PartyB': business_short_code,
                    'PhoneNumber': phone_number,
                    'CallBackURL': callback_url,
                    'AccountReference': account_reference,
                    'TransactionDesc': transaction_desc
                }
                print("MY PAYLOAD ",stk_push_payload)
                try:                        
                    response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                    response.raise_for_status()   
                    # Raise exception for non-2xx status codes
                    response_data = response.json()
                    checkout_request_id = response_data['CheckoutRequestID']
                    response_code = response_data['ResponseCode'] 
                    if response_code == "0":
                        #dealing the transaction
                        transaction =Transaction()                    
                        transaction.mpesa_charge_id = checkout_request_id
                        transaction.user = self.request.user
                        transaction.phone_number = phone_number
                        transaction.amount = order.get_total()
                        transaction.save()

                        #assigning payment to the order
                        order_items = order.items.all()
                        order_items.update(ordered=True)
                        for item in order_items:
                           item.save()

                        #delivery time
                        ordered_date = timezone.now()

                        # Calculate delivery date (ordered_date + 4 days)
                        delivery_date = ordered_date + timedelta(days=4)
                        order.delivery_date=delivery_date

                        order.ordered =True
                        order.transaction = transaction
                        order.reference_code=create_ref_code()
                        order.save()
                        messages.success(self.request, "pending payment")                            
                        return redirect('core:confirm_details')
                    else:
                        messages.success(self.request, "STK failed or transaction and order didn't get saved.")                            
                        return redirect('core:check_error')
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': str(e)})
            else:
                messages.warning(self.request,'Access token not found.')
                return redirect('core:check_error')
        else:
            return JsonResponse({'error': 'Failed to retrieve access token.'})         

                       
class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form' : form
        }
        return render(self.request, "refund.html", context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            reference_code = form.cleaned_data.get('reference_code')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            #edit the order
            try:
                order = Order.objects.get(reference_code=reference_code)
                order.refund_requested= True
                order.save()

                #store the refund
                refund = Refund()
                refund.order =order
                refund.email = email
                refund.reason = message
                refund.save()

                messages.info(self.request, "Your request has been received.")
                return redirect("core:request_refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request_refund")

def confirm_details(request):    
    all_amount = Transaction.objects.filter(user=request.user).order_by('-id').first()
    order_number = Order.objects.filter(user=request.user).order_by('-id').first()
    user_address = Address.objects.filter(user=request.user).order_by('-id').first()
    return render(request, "confirm_details.html", {'address': user_address, 'order_number': order_number, 'all_amount': all_amount})
 

def check_error(request):
   return render(request, "error_check.html")

def qtrack_order(request):   
    try:
        track=TrackOrder()
        track.tracking_number=create_track_number()
        track.status_steps = [
            {"active": True, "icon": "check", "name": "Order confirmed"},
            {"active": False, "icon": "user", "name": "Picked by courier"},
            {"active": False, "icon": "truck", "name": "On the way"},
            {"active": False, "icon": "box", "name": "Ready for pickup"},
        ]
        track.save()
        order_number = Order.objects.filter(user=request.user).order_by('-id').first()
        track_number = TrackOrder.objects.filter(user=request.user).order_by('-id').first()  
        # Check if the request is coming from an admin and update the boolean fields accordingly
        if request.user.is_superuser and request.method == 'POST':
            if 'courier_approval' in request.POST:
                track_number.courier_approved = True
                track_number.save()
            elif 'on_the_way_approval' in request.POST:
                track_number.on_the_way_approved = True
                track_number.save()
            elif 'pickup_approval' in request.POST:
                track_number.ready_for_pickup_approved = True
                track_number.save()
            # Redirect to the same page after updating the approval status
            return redirect('track_order')
        return render(request, "track_orders.html", {'order_number': order_number,'track_number': track_number})
    except TrackOrder.DoesNotExist:
        return render(request, "order_not_found.html")  # Render a page for order not found
    
#--- new ---
def track_order(request):
    try:
        # Get or create TrackOrder instance for the current user
        track_number, created = TrackOrder.objects.get_or_create(user=request.user)
        
        # If the TrackOrder instance is newly created, initialize its fields
        if created:
            track_number.tracking_number = create_track_number()
            track_number.status_steps = [
                {"active": True, "icon": "check", "name": "Order confirmed"},
                {"active": False, "icon": "user", "name": "Picked by courier"},
                {"active": False, "icon": "truck", "name": "On the way"},
                {"active": False, "icon": "box", "name": "Ready for pickup"},
            ]
            track_number.save()
        
        # Retrieve the latest order for the current user
        order_number = Order.objects.filter(user=request.user).order_by('-id').first()

        # Check if the request is coming from an admin and update the boolean fields accordingly
        if request.user.is_superuser and request.method == 'POST':
            if 'confirmed_approval' in request.POST:
                track_number.confirmed_approved = True
                track_number.save()
            if 'courier_approval' in request.POST:
                track_number.courier_approved = True
                track_number.save()
            elif 'on_the_way_approval' in request.POST:
                track_number.on_the_way_approved = True
                track_number.save()
            elif 'pickup_approval' in request.POST:
                track_number.ready_for_pickup_approved = True
                track_number.save()
            # Redirect to the same page after updating the approval status
            return redirect('track_order')
        
        return render(request, "track_orders.html", {'order_number': order_number,'track_number': track_number})
    
    except TrackOrder.DoesNotExist:
        return render(request, "order_not_found.html")




def sorry(request):
   return render(request, "sorry.html")