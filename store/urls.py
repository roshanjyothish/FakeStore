from django.urls import path
from store import views


urlpatterns = [
    path('register/',views.Userregister.as_view(),name="register"),
    path('vregister/',views.Vendorregister.as_view()),
    path('log/',views.Userlogin.as_view(),name="signin"),
    path('add_category/',views.Add_category.as_view(),name="addcat"),
    path('add_product/',views.Add_product.as_view(),name="addproduct"),
    path('home/',views.Category_list.as_view(),name="home"),
    path('productlist/',views.Product_list.as_view(),name="productlist"),
    path('productdetail/<int:pk>',views.Product_detail.as_view(),name="productdetail"),
    path('productupdate/<int:pk>',views.Product_update.as_view(),name="productupdate"),
    path('categorydetail/<int:pk>',views.Category_detail.as_view(),name="categorydetail"),
    path('addtocart/<int:pk>',views.Addtocartview.as_view(),name="addtocart"),
    path('deleteitem/<int:pk>',views.Cartdelete.as_view(),name="cart_delete"),
    path('view_cart/',views.CartRedirect.as_view(),name="cart"),
    

]