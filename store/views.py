from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,ListView,DetailView,UpdateView
from store.forms import Userregisterform,Loginform,Categoryform,Productform,Orderform
from store.models import User,Categorymodel,Productmodel,Cart_model,Order
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator

# Create your views here.

def signin_required(fn):

    def wrapper(request,*args,**kwargs):

        if not request.user.is_authenticated:

            return redirect("signin")
        
        else:
            return fn(request,*args,**kwargs)
        
    return wrapper



def mylogin(fn):

    def wrapper(request,*args,**kwargs):

        id=kwargs.get("pk")

        data=Cart_model.objects.get(id=id)

        if data.user!=request.user:

            return redirect('signin')

        else:

            return fn(request,*args,**kwargs)
        

# CUSTOMER REGISTRATION

# lh:8000/register
class Userregister(View):

    def get(self,request,*args,**kwargs):

        form=Userregisterform()

        return render(request,"register.html",{'form':form})
    
    def post(self,request,*args,**kwargs):

        form=Userregisterform(request.POST)

        if form.is_valid():

            u_name=form.cleaned_data.get("username")    
            email=form.cleaned_data.get("email")
            password=form.cleaned_data.get("password")

            user=User.objects.create_user(username=u_name,email=email,password=password)

            subject='Welcome to FakeStore World'

            message=f'Hi {user.username} thank you for registering in FakeStore'

            email_from= settings.EMAIL_HOST_USER

            recipient_list= [user.email,]

            send_mail( subject, message, email_from, recipient_list )

        form=Userregisterform()

        return render(request,"register.html",{"form":form})
    


class Userlogin(View):

    def get(self,request,*args,**kwargs):

        form=Loginform()

        return render(request,"login.html",{'form':form})
    
    def post(self,request,*args,**kwargs):

        form=Loginform(request.POST)

        if form.is_valid():

            u_name=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')

            user_obj=authenticate(username=u_name,password=pwd)

            if user_obj:

                login(request,user_obj)
            form=Loginform()

            # return render(request,"login.html",{'form':form})
            return redirect('home')


class Userlogout(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")


class Vendorregister(View):

    def get(self,request,*args,**kwargs):

        form=Userregisterform

        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):

        form=Userregisterform(request.POST)

        if form.is_valid():

            User.objects.create_superuser(**form.cleaned_data)
        
        form=Userregisterform

        return render(request,"register.html",{"form":form})



class Add_category(CreateView):

    model=Categorymodel
    form_class=Categoryform
    template_name="category.html"
    success_url=reverse_lazy('register')


class Add_product(CreateView):

    model=Productmodel
    form_class=Productform
    template_name="product.html"
    success_url=reverse_lazy('register')


# ListView====READ

class Category_list(ListView):

    model=Categorymodel
    template_name='home.html'
    context_object_name="categories"


class Category_detail(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        data=Productmodel.objects.filter(product_category_id=id)

        return render(request,"productlist.html",{"products":data})
    

class  Product_list(ListView):

    model=Productmodel
    template_name='productlist.html'
    context_object_name="products"


class Product_detail(DetailView):

    model=Productmodel
    template_name='product_detail.html'
    context_object_name="productdetail"


class Product_update(UpdateView):

    model=Productmodel
    template_name="product.html"
    form_class=Productform
    success_url=reverse_lazy("home")


@method_decorator(signin_required,name="dispatch")
class Addtocartview(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        data=Productmodel.objects.get(id=id)
        # getting product object from table Productmodel using the id

        Cart_model.objects.create(user=request.user,product=data)
        # adding the product object to the Cart_model (eg:obj)

        cart_data=Cart_model.objects.filter(user=request.user)
        # filtering the objects from cart_model

        price=0
        for i in cart_data:

            # more than one object in Cart_model so using for loop for iterating
            if i.product and hasattr(i.product,'product_price'):

                # checking if the objects have the field product and does it have the connecting field product-price
                price+=i.product.product_price

        return render(request,"cart.html",{'c_data':cart_data,'price':price})
    

class CartRedirect(View):

    def get(self,request,*args,**kwargs):

        cart_data=Cart_model.objects.filter(user=request.user)

        price=0
        for i in cart_data:

            if i.product and hasattr(i.product,'product_price'):

                price+=i.product.product_price

        return render(request,"cart.html",{'c_data':cart_data,'price':price})

class Cartdelete(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Cart_model.objects.get(id=id).delete()

        return redirect('cart')
    

class Order_View(View):
    def get(self,request,args,*kwargs):
        id=kwargs.get('pk')
        data=Productmodel.objects.get(id=id)
        Cart_model.objects.create(user=request.user,product=data)
        form=Orderform()
        return render(request,'order.html',{'data':data,'form':form})
    def post(self,request,args,*kwargs):
        id=kwargs.get('pk')
        data=Productmodel.objects.get(id=id)
        form=Orderform(request.POST)
        if form.is_valid():
            Order.objects.create(user=request.user,product=data,**form.cleaned_data)
        return render(request,"order.html",{'data':data})
    
class Logout_View(View):
    def get(self,request,args,*kwargs):
        logout(request)
        return redirect('signin')
    
  
class Orderlist_View(View):
    def get(self,request,args,*kwargs):
        data=Order.objects.filter(user=request.user)
        return render(request,'orderlist.html',{'data':data})