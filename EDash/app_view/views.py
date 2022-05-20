
from django.forms import model_to_dict
from django.shortcuts import redirect, render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from .custom_class import GetModel, paginate_class
from .models import CashMemo, Catagory, Product,Order,Cart, Restriction
from .forms import CartForm, CatagoryForm, MemoForm, ProductForm, UserForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import json
from django.contrib.auth.models import User

# Create your views here.    

def Home(request):
    qty = []
    products = Product.objects.all()
    for product in products:
        qty.append(product.qty)
    total_product = Product.objects.all().count()
    total_customer = Cart.objects.all().exclude(id=2).count()
    total_catagory = Catagory.objects.all().count()
    total_stock = sum(qty)
    return render(request, "home.html", {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_catagory": total_catagory,
        "total_stock": total_stock
        })

# Manage & View all Proudct

class ProductView(View):
    def get(self, request, page_no=1):
        query = Product.objects.all().order_by("-date_added")
        cart = Cart.objects.all()
        query = paginate_class(query, 1, page_no)
        return render(request, "products.html", {"obj": query["query"], "cart": cart, "page_num": query["page_num"], "pages": query["pages"]})
    

# Retrive Product
def get_product(request, pk):
    if request.method == "GET":
        query = Product.objects.filter(id=pk)
        return render(request, "products.html", {"obj": query})

# Update Product
@method_decorator(login_required, name='dispatch')
class ProductUpdate(View):
    def get_obj(self, pk):
        obj = Product.objects.get(id=pk)
        return obj
    def get(self, reqeust, pk):
        form = ProductForm(instance=self.get_obj(pk))
        return render(reqeust, "addProduct.html", {"form": form, "location": "update_product"})
    def post(self, request, pk):
        form = ProductForm(request.POST, instance=self.get_obj(pk))
        form.save()
        return redirect("/products")
    
# Delete Products
@method_decorator(login_required, name='dispatch')
class ProductDelete(View):
    def get(self, reqeust, pk):
        obj = Product.objects.get(id=pk)
        obj.delete()
        print("Deleted")
        return redirect("/products")


# Add Product
@method_decorator(login_required, name='dispatch')
class ProductManager(View):
    def get(self, request):
        form = ProductForm()
        return render(request, "addProduct.html", {"form": form, "location": "add_product"})
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("/products")
        return render(request, "addProduct.html")

# Add Order
@method_decorator(login_required, name='dispatch')
class OrderManager(View):
    def get(self, request, pk):
        query = Cart.objects.get(id=pk)
        try:
            objs = []
            query2 = Order.objects.filter(cart_no=query, status=False)
            if query2.count() != 0:
                for q in query2:
                    obj = Product.objects.get(id=q.product_id)
                    obj = model_to_dict(obj)
                    obj["catagory"] = Catagory.objects.get(id=obj['catagory']).name
                    obj['qty'] = q.qty
                    obj['cart'] = pk
                    objs.append(obj)
            else:
                objs = False
            return JsonResponse({'obj': objs})
        except:
            return JsonResponse({"msg": "No Response"})
    
    def post(self, request, pk):
        query = Cart.objects.get(id=pk)
        data = json.load(request)
        order = Order.objects.get(status=False, cart_no=query, product=data['target'])
        product = Product.objects.get(id=data['target'])
        if data['func'] == 'del' and order.qty > 1:
            order.qty -= 1
            product.qty += 1
            product.save()
            order.save()
        elif(data['func'] == 'del' and order.qty == 1):
            order.delete()
        elif(data['func'] == 'add' and product.qty > 1):
            order.qty += 1
            product.qty -= 1
            product.save()
            order.save()
        elif(data['func'] == "change_status"):
            order.status = True
            order.save()
            return JsonResponse({"msg": "Order status is set to complete"})
        return JsonResponse({"qty": order.qty, 'p_qty': product.qty})
    



class ProductToOrder(View):
    def post(self, request):
        data = json.load(request)
        try:
            query = Product.objects.get(id=data["id"])
            cart_query = Cart.objects.get(id=data["order_id"])
            cart_query_2 = cart_query.order_set.filter(product=query, status=False).first()
            if cart_query_2 == [] or cart_query_2 == None:
                cart_query_2 = Order(cart_no=cart_query, product=query, status=False )
            cart_query_2.qty += int(data["qty"])
            query.qty -= int(data["qty"])
            if not query.qty <=1:
                cart_query_2.save()
                query.save()
                return JsonResponse({"p_qty": query.qty, "o_qty": cart_query_2.qty, "id": query.id })
            else:
                return JsonResponse({"msg": 'Max Quantity Reached Decrease the Ammount'})
        except:
            return JsonResponse({"msg": 'No Object'})


class CartManager(GetModel):
    model = Cart
    template = "carts.html"
    form = CartForm
    redirect_link = "/carts/page=1"
    
class CatagoryManager(GetModel):
    model = Catagory
    template = "catagory.html"
    form = CatagoryForm
    redirect_link = "/catagorys"
    
# user manager

def log_out(request):
    logout(request)
    return redirect("/")

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("/")
        except:
            messages.error(request, "Username & Password is incorrect")
            return redirect("/login")
    else:
        return render(request, "user_login.html")

def register(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, 'user_reg.html', {"form": form, "action": "reg"})
    else:
        data = request.POST.copy()
        user = User.objects.all().filter(username=data["username"]).exists()
        print(user)
        if not user:
            data['password'] = make_password(data["password"])
            form = UserForm(data)
            try:
                form.save()
                return redirect("/")
            except:
                return HttpResponse("<h1>404 Somthing Went Wrong...</h1>")
        else:
            messages.warning(request, "Username already exists")
            return redirect("/signup")

def user_update(request):
    if request.method == "GET":
        user = User.objects.get(id=request.user.id)
        form = UserForm(instance=user)
        return render(request, "user_reg.html", {"form": form})
    else:
        user = User.objects.get(id=request.user.id)
        post_req = request.POST.copy()
        post_req["password"] = request.user.password
        form = UserForm(data= post_req, instance=request.user)
        if form.is_valid:
            form.save()
            return redirect("/")
        else:
            return HttpResponse("<h1>404 Error</h1>")


def change_password(request):
    if request.method == "POST":
        new_pass = request.POST["password"]
        if check_password(new_pass, request.user.password):
            pass_status = Restriction.objects.get(id=1)
            pass_status.value = True
            pass_status.save()
            return redirect("/update_password")
        else:
            messages.error(request, "Wrong Password")
            return redirect("/change_password")
    else:
        return render(request, "password_change.html")

def update_password(request):
    if request.method == "POST":
        new_pass = request.POST["password"]
        conf_pass = request.POST["conf_password"]
        if new_pass != conf_pass:
            messages.error(request, "password didn't match")
            redirect("/update_password")
        else:
            if len(new_pass) < 8:
                messages.error("At least 8 Character")
                redirect("/update_password")
            else:
                user = User.objects.get(id=request.user.id)
                user.set_password(new_pass)
                user.save()
                pass_status = Restriction.objects.get(id=1)
                pass_status.value = False
                pass_status.save()
                return redirect('/')
    else:
        pass_status = Restriction.objects.get(id=1)
        if pass_status.value == True:
            return render(request, "password_change.html")
        else:
            return redirect("/change_password")
# Cash Memo View

class MemoView(View):
    def get(self, request, page):
        query = CashMemo.objects.all().order_by("id")
        obj = paginate_class(query, 1, page)
        form = MemoForm()
        obj["form"] = form
        return render(request, "memoList.html", obj)
    def post(self, request):
        form = MemoForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("/memo/page=1")
        else:
            return HttpResponse("<h1>No Response</h1>")
    
class GetMemo(View):
    def get(self, request, pk):
        query = CashMemo.objects.get(id=pk)
        order = Order.objects.all().filter(cash_memo=query.id, cart_no=query.cart_no)
        cart = Cart.objects.get(id=query.cart_no_id)
        product = []
        total_ammount = []
        for o in order:
            p = Product.objects.get(id=o.product_id)
            p = model_to_dict(p)
            p["catagory"] = Catagory.objects.get(id=p["catagory"]).name
            p["qty_order"] = o.qty
            p["total_ammount"] = o.qty * p["retail"]
            total_ammount.append(p["total_ammount"])
            product.append(p)
        form = MemoForm(instance=query)
        return render(request, "memoView.html", {"cash_memo": query, "order": order, "cart":cart, "product": product, "total": sum(total_ammount)})
        
class MemoUpdate(View):
    def get(self, request, pk, page=0):
        query = CashMemo.objects.all().filter(id=pk)
        form = MemoForm(instance=query.first())
        return render(request, "memoList.html", {"query": query, "form" : form})
    def post(self, request, pk, page=0):
        query = CashMemo.objects.get(id=pk)
        form = MemoForm(data=request.POST, instance=query)
        if form.is_valid:
            form.save()
            return redirect("/memo/page=1")
        else:
            return HttpResponse("<h1>No Response</h1>")
        
        