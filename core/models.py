from django.db import models 
from django.conf import settings
from django.shortcuts import reverse


# Create your models here.
CATEGORY_CHOICES = (
   ('chr', 'Chrysanthemum'),
   ('rs', 'Rose'),
   ('dh', 'Dalhi'),
   ('sf', 'Sunflower'),
   ('mg', 'Marigold'),
   ('pp', 'Poppy'),
   ('mb', 'Mix Bunch'),
   ('ll', 'Lily')
)

LABEL_CHOICES = (
   ('lchr', 'LG chrysan'),
   ('lrs', 'LG Rose'),
   ('ldh', 'LG Dalhi'),
   ('lsf', 'LG Sunflower'),
   ('lmg', 'LG Marigold'),
   ('lpp', 'LG Poppy'),
   ('lmb', 'LG Mix Bunch'),
   ('lil', 'LG Lily')
)

ADDRESS_CHOICES = (
   ('B', 'Billing'),
   ('S', 'Shipping'),   
)


class Item(models.Model):
  title = models.CharField(max_length=100)
  image_title = models.CharField(max_length=100)
  cover = models.ImageField(upload_to='images/')
  price = models.FloatField()
  old_price = models.FloatField()
  discount_price = models.FloatField(blank = True, null = True )
  category = models.CharField(choices = CATEGORY_CHOICES, max_length = 3)
  label = models.CharField(choices = LABEL_CHOICES, max_length = 4)
  slug = models.SlugField() 
  description = models.TextField()  
  brief_description = models.TextField()
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse("core:product", kwargs = {
      'slug': self.slug })
  
  def get_add_to_cart_url(self):
    return reverse("core:add_to_cart", kwargs = {
      'slug': self.slug })
  
  def get_remove_from_cart_url(self):
    return reverse("core:remove_from_cart", kwargs = {
      'slug': self.slug })


class OrderItem(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  ordered = models.BooleanField(default=False)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)

  def __str__(self):
    return f"{self.quantity} of {self.item.title}"
  
  def get_total_item_price(self):
    return (self.item.price - self.item.discount_price) * self.quantity
  
  def get_final_price(self):
    return self.get_total_item_price()
  
  

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
  reference_code = models.CharField(max_length=40, blank=True, null=True)
  items = models.ManyToManyField(OrderItem)
  start_date = models.DateTimeField(auto_now_add=True)
  ordered_date = models.DateTimeField()
  ordered = models.BooleanField(default=False)
  shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
  transaction = models.ForeignKey('Transaction', on_delete=models.SET_NULL, blank=True, null=True)
  being_delivered = models.BooleanField(default=False)
  received = models.BooleanField(default=False)
  refund_requested = models.BooleanField(default=False)
  refund_granted = models.BooleanField(default=False)
  
  def __str__(self):
    return self.user.username
  
  def get_total(self):
    total = 0
    for order_item in self.items.all():
      total += order_item.get_final_price()
    return total
  
class Checkout(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
  town_address = models.CharField(max_length=100)
  pick_station = models.CharField(max_length=100)
  county = models.CharField(max_length=50)
  zip = models.CharField(max_length=100)  

  def __str__(self):
    return self.user.username  
    

class Address(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
  town_address = models.CharField(max_length=100)
  pick_station = models.CharField(max_length=100)
  county = models.CharField(max_length=50)
  zip = models.CharField(max_length=100)
  address_type = models.CharField(max_length=1, choices= ADDRESS_CHOICES)
  default =models.BooleanField(default=False)

  def __str__(self):
    return self.user.username
  
  class Meta:
    verbose_name_plural = 'Addresses'


class Transaction(models.Model):
    mpesa_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=100)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Refund(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  reason = models.TextField()
  accepted = models.BooleanField(default=False)
  email = models.EmailField()

  def __str__(self):
    return f"{self.pk}"