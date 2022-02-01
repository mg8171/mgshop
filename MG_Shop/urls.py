"""MG_Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.loginPage),
    path('contact/',views.contactPage),
    path('cart/',views.cartPage),
    path('deleteCart/<int:num>/',views.deleteCart),
    path('checkout/',views.checkoutPage),
    path('confirmation/',views.confirmation),
    path('product/<int:num>/',views.productDeails),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shopPage),
    path('signup/',views.signup),
    path('profile/',views.profile),
    path('sellerprofile/',views.sellerprofile),
    path('buyerprofile/',views.buyerprofile),
    path('addproduct/',views.addproduct),
    path('editProduct/<int:num>/',views.editProduct),
    path('deleteProduct/<int:num>/',views.deleteProduct),
    path('logout/',views.logout),
    path('editProfile/',views.editProfile),
    path('editProfile2/',views.editProfile2),
    path("wishlist/<int:num>/",views.wishlistPage),
    path('deletewishlist/<int:num>/',views.deleteWishlist),
    path('forgetpassword/',views.forgetPassword),
    path('enterOtp/<str:username>/',views.enterOtp),
    path('resetpassword/<str:username>/',views.resetPassword),
    path('paymentSucesss/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentSucesss),
    path('paymentFail/',views.paymentFail),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
