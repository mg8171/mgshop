from django.contrib import auth
from django.db.models.query_utils import Q
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,send_mass_mail
from random import randint
from django.contrib.sites.shortcuts import get_current_site
from MG_Shop.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay 
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    data = Product.objects.all()
    if(request.method=="POST"):
        nl = NewsLetter()
        nl.email=request.POST.get('email')
        subject = "NewsLetter Subscription Successfully"
        body =  """
                    Hello!!!!
                    Thank to subscribe our NewsLetter Service
                    Now you got an email when a new product
                    in listed in our website

                    Team:   MG_Shop
                """
        send_mail(subject, body,"mgshopsdjango@gmail.com",[nl.email,], fail_silently=False)
        nl.save()
        return HttpResponseRedirect("/")
    return render(request,"index.html",{"Data":data})

def cartPage(request):
    status = request.session.get("status",None)
    if(status==True):
        request.session["cart"]={}
    cart = request.session.get("cart",None)
    if(request.method=="POST"):
        q = int(request.POST.get('q'))
        if(q>0):
            num = request.POST.get('pid')
            cart[str(num)]=q
            request.session['cart']=cart
    cart = request.session.get("cart",None)
    if(cart):
        keys = cart.keys()
        product = []
        sum = 0
        for i in keys:
            p = Product.objects.get(pid=i)
            product.append(p)
            sum = sum+p.finalPrice*cart[i]
        if(sum<1000):
            shipping = 150
            final = sum+shipping
            
        else:
            shipping = False
            final = sum
    else:
        product=[]
        sum=0
        final = 0
        shipping = False
    return render(request,"cart.html",{"Product":product,"Total":sum, "Shipping":shipping,"Final":final})

def deleteCart(request,num):
    cart = request.session.get('cart',None)
    if(cart):
        cart.pop(str(num))
        request.session["cart"]=cart
    return HttpResponseRedirect('/cart/')

client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login/')
def checkoutPage(request):
    buyer = Buyer.objects.get(username=request.user)
    cart = request.session.get("cart",None)
    keys = cart.keys()
    product = []
    sum = 0
    for i in keys:
        p = Product.objects.get(pid=i)
        product.append(p)
        sum = sum+p.finalPrice*cart[i]
    if(sum<1000):
        shipping = 150
        final = sum+shipping
    else:
        shipping = False
        final = sum

    if(request.method=="POST"):
        check = CheckOut()
        check.buyer = buyer
        check.total = 0
        check.shipping = 0
        check.final = 0
        check.active=False
        check.save()

        check = CheckOut.objects.filter(buyer=buyer)
        check=check[::-1]
        check=check[0]
        check.buyer = buyer
        for i in product:
            check.product.add(i.pid)
        check.total = sum
        check.shipping = shipping
        check.final = final
        for i in product:
            check.q = check.q+str(i.pid)+":"+str(cart[str(i.pid)])+","
        check.mode = request.POST.get('mode')
        if(check.mode=="cod"):
            check.active=True
            check.save()
            if(request.session.get("status",None)!=None):
                request.session['status']=True
            subject = "Your Order is placed Successfully"
            body =  """
                    Hello!!!!
                    Thank to for Shopping with US
                    Team:   MG_Shop
                    http://localhost:8000
                    """
            send_mail(subject, body,"mgshopsdjango@gmail.com",[buyer.email,], fail_silently=False)
            return HttpResponseRedirect('/confirmation/')
        else:
            orderAmount = check.final*100
            orderCurrency = "INR"
            paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
            paymentId = paymentOrder['id']
            check.active=True
            check.order_id=paymentId
            check.save()
            return render(request,"pay.html",{
                "amount":orderAmount,
                "api_key":RAZORPAY_API_KEY,
                "order_id":paymentId
            })
    return render(request,"checkout.html",{"User":buyer,"Product":product,"Total":sum,"Shipping":shipping,"Final":final})

@login_required(login_url='/login/')
def paymentSucesss(request,rppid,rpoid,rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = CheckOut.objects.filter(buyer=buyer)
    check=check[::-1]
    check=check[0]
    check.razorpay_payment_id=rppid
    check.razorpay_order_id=rpoid
    check.razorpay_signature=rpsid
    check.payment_status=1
    check.save()
    if(request.session.get("status",None)!=None):
        request.session['status']=True
    subject = "Your Order is placed Successfully"
    body =  """
            Hello!!!!
            Thank to for Shopping with US
            Team:   MG_Shop
            http://localhost:8000
            """
    send_mail(subject, body,"mgshopsdjango@gmail.com",[buyer.email,], fail_silently=False)
    return HttpResponseRedirect('/confirmation/')

@login_required(login_url='/login/')
def paymentFail(request):
    buyer = Buyer.objects.get(username=request.user)
    check = CheckOut.objects.filter(buyer=buyer)
    check=check[::-1]
    check=check[0]
    check.payment_status=2
    check.save()
    if(request.session.get("status",None)!=None):
        request.session['status']=True
    subject = "Your Payment is Fail"
    body =  """
            OOPs Payment Fail!!!!
            Please try Again
            Thank to for Shopping with US
            Team:   MG_Shop
            http://localhost:8000
            """
    send_mail(subject, body,"mgshopsdjango@gmail.com",[buyer.email,], fail_silently=False)
    return render(request,"paymentFail.html")

@login_required(login_url='/login/')
def payment_cancelled(request):
    return render(request,"/")


@login_required(login_url='/login/')
def confirmation(request):
    buyer = Buyer.objects.get(username=request.user)
    check = CheckOut.objects.filter(buyer=buyer)
    check = check[::-1]
    check = check[0]
    product = []
    for i in check.product.all():
        product.append(i)
    total = check.total
    shipping = check.shipping
    final = check.final
    
    return render(request,"confirmation.html",{"OrderNo":check.cid,"Product":product,"Total":total,"Shipping":shipping,"Final":final,"Buyer":buyer})

def contactPage(request):
    if(request.method=="POST"):
        c = ContactUs()
        c.name = request.POST.get('name')
        c.email = request.POST.get('email')
        c.subject = request.POST.get('subject')
        c.message = request.POST.get('message')
        c.save()
        return HttpResponseRedirect("/")
    return render(request,"contact.html")

def loginPage(request):
    if(request.method=="POST"):
        uname = request.POST.get('username')
        pward = request.POST.get('password')
        user = authenticate(username=uname,password=pward)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/admin/')
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid Username or Password")

    return render(request,"login.html")

def productDeails(request,num):
    product = Product.objects.get(pid=num)
    if(request.method=="POST"):
        q = int(request.POST.get('qty'))
        cart = request.session.get('cart',None)
        if(cart):
            cartProducts = cart.keys()
            if(product.pid in cartProducts):
                cart[product.pid]=q
            else:
                cart.setdefault(product.pid,q)
        else:
            cart = {product.pid:q}
        try:
           buyer = Buyer.objects.get(username=request.user)
           wish = WishList.objects.get(buyer=buyer,product=product)
           wish.delete()
        except:
            pass

        request.session["cart"]=cart
        request.session['status']=False
        return HttpResponseRedirect("/cart/")
    return render(request,"product.html",{"Product":product})

def shopPage(request,mc,sc,br):
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    if(mc=="None" and sc=="None" and br=="None"):
        products = Product.objects.all()
    elif(mc!="None" and sc=="None" and br=="None"):
        products = Product.objects.filter(mainCat=mc)
    elif(mc=="None" and sc!="None" and br=="None"):
        products = Product.objects.filter(subCat=sc)
    elif(mc=="None" and sc=="None" and br!="None"):
        products = Product.objects.filter(brand=br)
    elif(mc!="None" and sc!="None" and br=="None"):
        products = Product.objects.filter(mainCat=mc,subCat=sc)
    elif(mc!="None" and sc=="None" and br!="None"):
        products = Product.objects.filter(mainCat=mc,brand=br)
    elif(mc=="None" and sc!="None" and br!="None"):
        products = Product.objects.filter(subCat=sc,brand=br)
    else:
        products = Product.objects.filter(mainCat=mc,subCat=sc,brand=br)
    return render(request,"shop.html",{"MainCat":mainCat,"SubCat":subCat,"Brand":brand,
                                       "MC":mc,"SC":sc,"BR":br,"Product":products})

def signup(request):
    if(request.method=="POST"):
        if(request.POST.get("accountType")=="seller"):
            s = SELLER()
            s.name = request.POST.get("name")
            uname = s.username = request.POST.get("username")
            pward = request.POST.get("password")
            s.email = request.POST.get("email")
            s.phone = request.POST.get("phone")
            s.pic = request.FILES.get("pic")
            user = User.objects.create_user(username=uname,password=pward)
            user.save()
            s.save()
        else:
            b = Buyer()
            b.name = request.POST.get("name")
            uname = b.username = request.POST.get("username")
            pward = request.POST.get("password")
            b.email = request.POST.get("email")
            b.phone = request.POST.get("phone")
            b.pic = request.FILES.get("pic")
            user = User.objects.create_user(username=uname,password=pward)
            user.save()
            b.save()
        return HttpResponseRedirect('/profile/')      
    return render(request,"signup.html")

@login_required(login_url='/login/')
def profile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        try:
            seller = SELLER.objects.get(username=request.user)
            return HttpResponseRedirect('/sellerprofile/')
        except:
            buyer = Buyer.objects.get(username=request.user)
            return HttpResponseRedirect('/buyerprofile/')


@login_required(login_url='/login/')
def sellerprofile(request):
    seller = SELLER.objects.get(username=request.user)
    product = Product.objects.filter(seller=seller)
    return render(request,'sellerprofile.html',{'User':seller,"Product":product})

@login_required(login_url='/login/')
def buyerprofile(request):
    buyer = Buyer.objects.get(username=request.user)
    product = WishList.objects.filter(buyer=buyer)
    return render(request,'buyerprofile.html',{'User':buyer,"Product":product})

@login_required(login_url='/login/')
def addproduct(request):
    if(request.method=="POST"):
        p = Product()
        p.name = request.POST.get("name")
        p.basePrice = int(request.POST.get("basePrice"))
        p.discount = int(request.POST.get("discount"))
        p.finalPrice = p.basePrice-p.basePrice*p.discount/100
        p.mainCat = MainCategory.objects.get(name=request.POST.get("mc"))
        p.subCat = SubCategory.objects.get(name=request.POST.get("sc"))
        p.brand = Brand.objects.get(name=request.POST.get("br"))
        p.seller = SELLER.objects.get(username=request.user)
        p.stock = bool(request.POST.get("stock"))
        p.desc = request.POST.get("desc")
        p.specification = request.POST.get("specification")
        p.color = request.POST.get("color")
        p.number = request.POST.get("number")
        p.pic1 = request.FILES.get("pic1")
        p.pic2 = request.FILES.get("pic2")
        p.pic3 = request.FILES.get("pic3")
        p.pic4 = request.FILES.get("pic4")
        p.pic5 = request.FILES.get("pic5")
        p.save()
        subject = "New product List on MG_Shop Chckout Now!!!!!"
        body =  """
                    Hello!!!!
                    Click on the link below to check our latest products
                    Team:   MG_Shop
                    http://localhost:8000/product/{}/
                    """.format(p.pid)
        for i in NewsLetter.objects.all():
            send_mail(subject, body,"mgshopsdjango@gmail.com",[i.email,],fail_silently=True)
        return HttpResponseRedirect('/profile/')
    mc = MainCategory.objects.all()
    sc = SubCategory.objects.all()
    br = Brand.objects.all()
    return render(request,"addproduct.html",{"MC":mc,"SC":sc,"BR":br})

@login_required(login_url='/login/')
def editProduct(request,num):
    p = Product.objects.get(pid=num)
    if(request.method=="POST"):
        p.name = request.POST.get("name")
        p.basePrice = int(request.POST.get("basePrice"))
        p.discount = int(request.POST.get("discount"))
        p.finalPrice = p.basePrice-p.basePrice*p.discount/100
        p.mainCat = MainCategory.objects.get(name=request.POST.get("mc"))
        p.subCat = SubCategory.objects.get(name=request.POST.get("sc"))
        p.brand = Brand.objects.get(name=request.POST.get("br"))
        p.seller = SELLER.objects.get(username=request.user)
        p.stock = bool(request.POST.get("stock"))
        p.desc = request.POST.get("desc")
        p.specification = request.POST.get("specification")
        p.color = request.POST.get("color")
        p.number = request.POST.get("number")
        if(not request.FILES.get("pic1")==None):
            p.pic1 = request.FILES.get("pic1")
        if(not request.FILES.get("pic2")==None):
            p.pic2 = request.FILES.get("pic2")
        if(not request.FILES.get("pic3")==None):
            p.pic3 = request.FILES.get("pic3")
        if(not request.FILES.get("pic4")==None):
            p.pic4 = request.FILES.get("pic4")
        if(not request.FILES.get("pic5")==None):
            p.pic5 = request.FILES.get("pic5")
        p.save()
        return HttpResponseRedirect('/profile/')
    mc = MainCategory.objects.all()
    sc = SubCategory.objects.all()
    br = Brand.objects.all()
    return render(request,"editproduct.html",{"Product":p,"MC":mc,"SC":sc,"BR":br})

@login_required(login_url='/login/')
def deleteProduct(request,num):
    product = Product.objects.get(pid=num)
    seller = SELLER.objects.get(username=request.user)
    if(product.seller==seller):
        product.delete()
        return HttpResponseRedirect("/sellerprofile/")
    else:
        return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def editProfile(request):
    s = SELLER.objects.get(username=request.user)
    if(request.method=="POST"):
        s.name = request.POST.get("name")
        s.email = request.POST.get("email")
        s.phone = request.POST.get("phone")
        if(not request.FILES.get("pic")==None):
            s.pic = request.FILES.get("pic")
        s.save()
        return HttpResponseRedirect('/profile/') 
    return render(request,"editsellerprofile.html",{"User":s})

@login_required(login_url='/login/')
def editProfile2(request):
    b = Buyer.objects.get(username=request.user)
    if(request.method=="POST"):
        b.name = request.POST.get("name")
        b.email = request.POST.get("email")
        b.phone = request.POST.get("phone")
        b.addressLine1 = request.POST.get("addressLine1")
        b.addressLine2 = request.POST.get("addressLine2")
        b.addressLine3 = request.POST.get("addressLine3")
        b.city = request.POST.get("city")
        b.state = request.POST.get("state")
        b.pin = request.POST.get("pin")
        if(not request.FILES.get("pic")==None):
            b.pic = request.FILES.get("pic")
        b.save()
        return HttpResponseRedirect('/profile/') 
    return render(request,"editprofileB.html",{"User":b})

@login_required(login_url='/login/')
def wishlistPage(request,num):
    product = Product.objects.get(pid=num)
    buyer = Buyer.objects.get(username = request.user)
    buyerwish = WishList.objects.filter(buyer=buyer)
    flag=False
    for i in buyerwish:
        if(product==i.product):
            flag=True
    if(flag==False):
        w = WishList()
        w.product=product
        w.buyer=buyer
        w.save()
    return HttpResponseRedirect('/buyerprofile/')

@login_required(login_url='/login/')
def deleteWishlist(request,num):
    wishlist = WishList.objects.get(wid=num)
    buyer = Buyer.objects.get(username = request.user)
    if(wishlist.buyer==buyer):
        wishlist.delete()
    return HttpResponseRedirect('/buyerprofile/')

def forgetPassword(request):
    if(request.method=="POST"):
        flag = False
        username = request.POST.get("username")
        try:
            user = SELLER.objects.get(username=username)
            flag=True
        except:
            try:
                user = Buyer.objects.get(username=username)
                flag=True
            except:
                pass

        if(flag==True):
            user.otp = randint(1000,9999)
            user.save()
            subject = "OTP for Password Reset"
            body =  """
                        Hello!!!!
                        Your OTP for PasssWord Rest is
                        {}
                        Team:   MG_Shop
                    """.format(user.otp)
            send_mail(subject, body,"mgshopsdjango@gmail.com",[user.email,], fail_silently=False)
            return HttpResponseRedirect('/enterOtp/'+username+"/")
        else:
            messages.error(request,"User Name not fund")
    return render(request,"forgetpassword1.html")

def enterOtp(request,username):
    if(request.method=="POST"):
        flag = False
        otp = int(request.POST.get("otp"))
        try:
            user = SELLER.objects.get(username=username)
            flag=True
        except:
            try:
                user = Buyer.objects.get(username=username)
                flag=True
            except:
                pass

        if(flag==True):
            if(user.otp==otp):
                return HttpResponseRedirect('/resetpassword/'+username+"/")
            else:
                messages.error(request,"OTP Does't Match")    
        else:
            messages.error(request,"User Name not fund")
    return render(request,"otp.html")


def resetPassword(request,username):
    if(request.method=="POST"):
        password1 = request.POST.get("p1")
        password2 = request.POST.get("p2")
        # try:
        user = User.objects.get(username=username)
        if(password1==password2):
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            messages.error("Password and Confirm Password not Match")
        # except:
        #     messages.error(request,"User not fund")
    return render(request,"resetpassword.html")

