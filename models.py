from django.db import models
from django.contrib.auth.models import User
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.TextField(max_length=500)
    phonenumber = models.IntegerField()
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

    
class Product(models.Model):
    product_id = models.AutoField
    category = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=200, null=True, default="")
    price = models.IntegerField(default=0)
    digital = models.BooleanField(default=False,null=True,blank=False)
    desc = models.CharField(max_length=300)
    # in_stock  = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/images')
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def shipping(self):
        shipping =False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital ==False:
                shipping =True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = 0  
        for item in orderitems:
            total += item.get_total
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = 0  
        for item in orderitems:
            total += item.quantity
        return total

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.product:
            return self.product.name
        else:
            return f"OrderItem {self.id} (No product)"
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)  # Add this line for the state field
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

  
    def __str__(self):
        return f"{self.customer} - {self.address}, {self.city}, {self.state}, {self.zipcode}"
