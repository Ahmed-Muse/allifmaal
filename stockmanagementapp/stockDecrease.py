
'''
https://stackoverflow.com/questions/59147650/django-trouble-adjusting-stock-when-an-order-is-cancelled
So in my website when a user cancels an order I want the stock of the products that the user 
has bought to be brought back up, but whenever I test it the stock remains the same (But successfully decreases when
 a user buys something). The function I am trying to do this with is adjust_stock in order/views.py as follows:

''''
#below are the order models
from django.db import models
from shop.models import Product

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    emailAddress = models.EmailField(max_length=250, blank=True)

    class Meta:
        db_table = 'Order'
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_items(self):
        return OrderItem.objects.filter(order=self)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
#end of order models
#start of cart models
from django.db import models
from shop.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank = True)
    date_added = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product
#end of cart models

#these below codes are possible solutions... so try them out
from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order
from cart.models import Cart, CartItem
from cart.views import _cart_id
from shop.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import stripe

@login_required()
def order_create(request, total=0, cart_items = None):
    if request.method == 'POST':
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            total += (item.quantity * item.product.price)
        print('Total', total)
        charge = stripe.Charge.create(
            amount=str(int(total*100)),
            currency='EUR',
            description = 'Credit card charge',
            source=request.POST['stripeToken']
        )
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.create(emailAddress = email)
        order_details.save()


    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)#this is filtering and getting items of that particular cart...
        #same us InvPharmItems = InvoicePharmacyItemsModel.objects.filter(invoiceAndPharmacyItemsConnector=myInv)#fi
        for order_item in cart_items:
            oi = OrderItem.objects.create(
                product = order_item.product.name,
                quantity = order_item.quantity,
                price = order_item.product.price, 
                order = order_details)
        total += (order_item.quantity * order_item.product.price)
        oi.save()

        #Reduce stock when order is placed or saved
        products = Product.objects.get(id=order_item.product_id)
        if products.stock > 0:
            products.stock = int(order_item.product.stock - order_item.quantity)
        products.save()
        order_item.delete()
    except ObjectDoesNotExist:
        pass
    return render(request, 'order.html', dict(cart_items = cart_items, total=total))

def adjust_stock(id, quantity):
    products = Product.objects.filter(id=id)
    products.stock = int(product.stock + quantity)
    products.save()



@login_required()
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(emailAddress=email)
    paginator = Paginator(order_details, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        orders = paginator.page(page)
    except (EmptyPage, InvalidPage):
        orders = paginator.page(paginator.num_pages)
    return render(request, 'orders_list.html', {'orders':orders})




def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_date = order.created
    current_date = datetime.now(timezone.utc)
    date_diff = current_date - order_date
    minutes_diff = date_diff.total_seconds() / 60.0
    order_items = OrderItem.objects.filter(id=order_id)
    if minutes_diff <= 30:
        for product in order_items:
            product.adjust_stock(order_items.product.id, order_items.quantity)



        order.delete()
        messages.add_message(request, messages.INFO,
                        'Your order is cancelled.')
    else:
        messages.add_message(request, messages.INFO,
                        'Sorry, it is too late to cancel this order.')
    return redirect('order_history')




#below is cart view like another app
def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total*100)
    description = 'MyTea - Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'cart.html', dict(cart_items = cart_items, total = total, 
                    counter = counter, data_key = data_key, stripe_total = stripe_total, description = description))

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def full_remove(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        cart_item.delete()
    return redirect('cart_detail')
#end of cart views.py