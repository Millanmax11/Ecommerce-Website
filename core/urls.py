from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name = 'homepage'),
    path('account_login/', views.account_login, name="login"),
    path('custom_login/', views.custom_login, name="custom_login"),
    path('custom_signup/', views.custom_signup, name="custom_signup"),
    path('homepage/', views.HomeView.as_view(), name = 'homepage'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),     
    path('blog/', views.blog, name="blog"),
    path('cart/', views.cart, name="cart"),

    path('product/<slug>/', views.ItemDetailView.as_view(), name = 'product'),
    path('add_to_cart/<slug>/', views.add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<slug>/', views.remove_from_cart, name = 'remove_from_cart'),
    path('remove_single_from_cart/<slug>/', views.remove_single_from_cart, name = 'remove_single_from_cart'),
    path('order_summary/', views.OrderSummeryView.as_view(), name="order_summary"),
    path('remove_single_item_from_cart/<slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('add_single_item_to_cart/<slug>/', views.add_single_item_to_cart, name ='add_single_item_to_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name="payment"),
    path('get_address_details/', views.get_address_details, name="get_address_details"),

    path('check_error/', views.check_error, name="check_error"), 
    path('confirm_details/', views.confirm_details, name="confirm_details"),
    path('track_orders/', views.track_order, name="track_orders"),
    path('upload/', views.upload_image, name='upload'),
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('request_refund/', views.RequestRefundView.as_view(), name='request_refund'),


    path('sorry/', views.sorry, name='sorry')

    
]