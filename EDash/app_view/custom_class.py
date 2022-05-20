from re import T
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

# Simple Function of Pagination
def paginate_class(obj, item_numbers, page_no):
    from django.core.paginator import Paginator
    paginate = Paginator(obj, item_numbers)
    page_num = paginate.num_pages
    page_list = []
    for page in range(page_num + 1):
        if page != 0 and page_no <= page <= page_no+10:
            page_list.append(page)
    return {"query":paginate.page(page_no), "page_num": page_list, "pages": page_num}

class GetModel(View):
    model = ""
    template = ""
    form = ""
    redirect_link = "/"
    def get(self, request, pk="all", act=None, page=1):
        context = {}
        def tryObj(object):
            try:
                obj = object
            except ValueError or TypeError:
                obj = "No model added"
            return obj
        if(pk == "all"):            
            query = tryObj(self.model.objects.all().order_by('id'))
            query = paginate_class(query, 1, page)
            form = tryObj(self.form())
            context = query
            context["form"] = form
            return render(request, self.template, context=context)
        elif(act == "delete" and pk != "all"):
            query = tryObj(self.model.objects.filter(id=pk))
            query.delete()
            return redirect("/carts")
        else:
            query = tryObj(self.model.objects.all().filter(id=pk))
            form = tryObj(self.form(instance=query.first()))
        context["query"] = query
        context["form"] = form
        return render(request, self.template, context )
    def post(self, request, page, pk="all", act=None):
        if(pk== "all"):
            form = self.form(request.POST)
        else:
            query = self.model.objects.get(id=pk)
            form = self.form(request.POST, instance=query)
        if form.is_valid:
            form.save()
            return redirect(self.redirect_link)
        else:
            return HttpResponse("<h1 style='text-align:center'>Someting Went worng with submission</h1>")