from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register((MainCategory,SubCategory,Product,Brand,SELLER,Buyer,WishList,CheckOut,ContactUs,NewsLetter))
