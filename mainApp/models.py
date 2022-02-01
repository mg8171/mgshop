from django.db import models
from django.db.models.fields import EmailField
from django.db.models.fields.related import ForeignKey

# Create your models here.
class MainCategory(models.Model):
    mid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Brand(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SELLER(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15,default=None,null=True,blank=True)
    otp = models.IntegerField(default=0,blank=True,null=True)
    pic = models.ImageField(upload_to='images/',default=None,null=True,blank=True)
    
    def __str__(self):
        return str(self.sid)+' '+self.name

class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    basePrice = models.IntegerField()
    discount = models.IntegerField(default=0,blank=True,null=True)
    finalPrice = models.IntegerField()
    mainCat = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    subCat = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,default=None)
    seller = models.ForeignKey(SELLER,on_delete=models.CASCADE)
    stock = models.BooleanField(default=True)
    desc = models.TextField()
    specification = models.TextField()
    color = models.CharField(max_length=20)
    number = models.IntegerField()
    pic1 = models.ImageField(upload_to='images/',default=None,null=True,blank=True)
    pic2 = models.ImageField(upload_to='images/',default=None,null=True,blank=True)
    pic3 = models.ImageField(upload_to='images/',default=None,null=True,blank=True)
    pic4 = models.ImageField(upload_to='images/',default=None,null=True,blank=True)
    pic5 = models.ImageField(upload_to='images/',default=None,null=True,blank=True)

    def __str__(self):
        return str(self.pid)+" "+self.name

class Buyer(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15,default=None,null=True,blank=True)
    pic = models.ImageField(upload_to='images/',default=None,null=True,blank=True)
    addressLine1 = models.CharField(max_length=50,default=None,null=True)
    addressLine2 = models.CharField(max_length=50,default=None,null=True)
    addressLine3 = models.CharField(max_length=50,default=None,null=True)
    city = models.CharField(max_length=50,default=None,null=True)
    state = models.CharField(max_length=50,default=None,null=True)
    pin = models.CharField(max_length=50,default=None,null=True)
    otp = models.IntegerField(default=0,blank=True,null=True)
    
    def __str__(self):
        return str(self.bid)+' '+self.name

class WishList(models.Model):
    wid = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.wid)+" "+self.buyer.name

class CheckOut(models.Model):
    cid = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,default=1)
    total = models.IntegerField()
    shipping = models.IntegerField(default=0,null=True,blank=True)
    final = models.IntegerField()
    active = models.BooleanField(default=True)
    q = models.TextField(default="")
    mode = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now=True)
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    status = models.IntegerField(choices = status_choices, default=1)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.cid)+"\t"+self.buyer.username+"\t"+str(self.active)

class ContactUs(models.Model):
    cuid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.cuid)+" "+self.subject

class NewsLetter(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField()

    def __str__(self):
        return str(self.nid)+" "+self.email
