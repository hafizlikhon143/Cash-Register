from django.urls import path
from django.shortcuts import redirect
from .views import *

def reDirToFirst(request):
    return redirect("/products/page=1")

urlpatterns = [
    path("", Home, name="home"),
    path("products", reDirToFirst),
    path("products/page=<int:page_no>", ProductView.as_view()),
    path("product/<str:pk>", get_product),
    path("add_product", ProductManager.as_view(), name="Add Product"),
    path('update_product/<int:pk>', ProductUpdate.as_view(), name="Update Product"),
    path("product/<int:pk>/delete", ProductDelete.as_view()),
    path("order_data/<int:pk>", OrderManager.as_view()),
    path("order_product", ProductToOrder.as_view()),
    path("carts/page=<int:page>", CartManager.as_view()),
    path("cart/<int:pk>", CartManager.as_view()),
    path("cart/<int:pk>/<str:act>", CatagoryManager.as_view()),
    path("catagorys/page=<int:page>", CatagoryManager.as_view()),
    path("catagory/<int:pk>", CatagoryManager.as_view()),
    path("catagory/<int:pk>/<str:act>", CatagoryManager.as_view()),
    path("memo/page=<int:page>", MemoView.as_view()),
    path("memo/<int:pk>", GetMemo.as_view()),
    path("memo/<int:pk>/update", MemoUpdate.as_view(), name="Memo_Update"),
    path("user/update", user_update),
    path("change_password", change_password),
    path("update_password", update_password),
    path("logout", log_out, name="LOG_OUT"),
    path("login", log_in, name="LOGIN"),
    path("signup", register, name="SIGNUP"),
]
