# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required, login_required
from django.template.loader import render_to_string
from SADProject.myUser.backend import MyBackend
from SADProject.orders.views import changeQuerySet
from SADProject.settings import MEDIA_ROOT
from models import Category
from django.http import *
from SADProject.orders.models import OrderItem
from SADProject.orders.models import Order
from SADProject.utils.templatetags.tags import good_cats
from models import Good
from SADProject.myUser import inform_trustee,inform_user
from django.http import HttpResponse
import datetime
import json
import os

from django_jalali.db.models import jDateField
from django.shortcuts import render_to_response
from SADProject.utils.view_utils import render_to_response_wrapper, jsonListGenerator, deleteFromQuerySet


def save_upload( uploaded, filename, raw_data ):
    '''
    raw_data: if True, uploaded is an HttpRequest object with the file being
              the raw post data
              if False, uploaded has been submitted via the basic form
              submission and is a regular Django UploadedFile in request.FILES
    '''
    try:
        from io import FileIO, BufferedWriter

        with BufferedWriter(FileIO(os.path.join(MEDIA_ROOT, filename), "wb")) as dest:
            # if the "advanced" upload, read directly from the HTTP request
            # with the Django 1.3 functionality
            if raw_data:
                foo = uploaded.read(1024)
                while foo:
                    dest.write(foo)
                    foo = uploaded.read(1024)
            # if not raw, it was a form upload so read in the normal Django chunks fashion
            else:
                for c in uploaded.chunks():
                    dest.write(c)
                    # got through saving the upload, report success
            return True
    except IOError:

        # could not open the file most likely
        pass
    return False


@permission_required("warehouse.add_receipt")
def uploadAjax(request):
    if request.method == "POST":
        if request.is_ajax():
            # the file is stored raw in the request
            upload = request
            is_raw = True
            good = request.GET['good']
            # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
            try:
                filename = good + '.jpg'

            except KeyError:
                return HttpResponseBadRequest("AJAX request not valid")
        # not an ajax upload, so it was the "basic" iframe version with submission via form
        else:
            return

        # save the file
        success = save_upload(upload, filename, is_raw)

        if success:
            goodObject = Good.objects.get(pk=int(good))
            if goodObject.status == 'U' or goodObject.status == 'L':
                goodObject.status = 'L'
                goodObject.save()

            # let Ajax Upload know whether we saved it or not
        import json

        ret_json = {'success': success, }
        return HttpResponse(json.dumps(ret_json))

@permission_required("warehouse.view_my_goods")
def myGoodsView(request):
    return render_to_response_wrapper(request,template='myGoods.html')

@permission_required("warehouse.view_my_goods")
def myGoodsJson(request):
    columns = ['pk',  'category', 'submitDate', 'status']
    data = Good.objects.filter(user=request.user)
    my_dict = {'show_status': True}


    return jsonListGenerator(request=request, columns=columns, data=data, my_dict=my_dict,
                             template="json/allgoods.json")

@permission_required("warehouse.view_all_goods")
def allGoodsJson(request):
    columns = ['pk', 'user', 'category', 'submitDate', 'status']
    data = Good.objects.all()
    my_dict = {'show_status': True, 'show_user': True,'show_buttons' : True}
    if request.user.groups.all()[0].name == 'T':
        my_dict.update({'show_receipt': True})

    return jsonListGenerator(request=request, columns=columns, data=data, my_dict=my_dict,
                             template="json/allgoods.json")


@permission_required("warehouse.register_delivery")
def deliveryJson(request):
    columns = ['pk', 'user']
    data = Good.objects.filter(status='W')
    my_dict = {'show_user': False, 'checkbox': True, 'show_status': False}
    return jsonListGenerator(request=request, columns=columns, data=data, my_dict=my_dict,
                             template="json/allgoods.json")


@permission_required("warehouse.register_delivery")
def goodDeliveryView(request):
    my_dcit = { 'delivery_title': 'تحویل کالا' , 'final_delivery_address': '../finaldelivery/' , 'table_json_address' : '../json/delivery'}
    return render_to_response_wrapper(request, "gooddelivery.html",my_dcit)


@login_required
def categoriesJson(request):
    columns = ['name']
    data = Category.objects
    return jsonListGenerator(request=request, columns=columns, data=data, template="json/categories.json")


@permission_required("warehouse.change_categories")
def categoriesView(request):
    return render_to_response_wrapper(request, "categories.html")


@login_required
def categoryList(request):
    return HttpResponse(good_cats())


@permission_required("warehouse.change_categories")
def changeCategory(request):
    columns = ['name']
    changeQuerySet(request, columns, Category.objects)
    return HttpResponse('success')


@permission_required("warehouse.view_all_goods")
def changeGood(request):
    columns = ['user', 'category', 'status']
    changeQuerySet(request, columns, Good.objects)
    return HttpResponse('success')


@permission_required("warehouse.view_all_goods")
def deleteGood(request):
    deleteFromQuerySet(request, Good.objects)
    return HttpResponse('success')


@permission_required("warehouse.change_categories")
def deleteCategory(request):
    category = Category.objects.get(pk=int(request.POST['pk']))
    new_category = Category.objects.get(pk=int(request.POST['newpk']))
    Good.objects.filter(category=category).update(category=new_category)
    OrderItem.objects.filter(category=category).update(category=new_category)
    category.delete()
    return HttpResponse('success')


@permission_required("warehouse.change_categories")
def addCategory(request):
    Category(name=request.POST['name']).save()
    return HttpResponse('success')


@permission_required("warehouse.add_new_good")
def addGood(request):
    buy_agent = MyBackend().authenticate(request.POST['username'], request.POST['password'])
    if buy_agent == None or (buy_agent.groups.all()[0].name != 'B' and not buy_agent.is_superuser) :
        return HttpResponse('borooo')
    today = jDateField()
    today = today.to_python(datetime.datetime.now())

    order = Order.objects.filter(pk=int(request.POST['order']))[0]
    orderitem = OrderItem.objects.filter(pk=int(request.POST['orderitem']))[0]
    orderitem.status = 'I'
    orderitem.save()
    if not order.user == None:
        inform_user(user=order.user, message=render_to_string('mail/orderitem_available.html', {'orderitem': orderitem}),
                    subject='سفارش شما در انبار موجود است')

    if not OrderItem.objects.filter(order=order).exclude(status='I'):
        order.status = 'D'
        order.save()

    for i in range(0, orderitem.quantity):
        good = Good(submitDate=today, category=orderitem.category, user=order.user, orderitem=orderitem, status='W')
        good.save()

    c = {'rlink': '../../allgoods/', 'success': "کالاها با موفقیت ثبت شدند"}
    return render_to_response("success.html", c)


@permission_required("warehouse.add_new_good")
def addGoodView(request):
    return render_to_response_wrapper(request, "addgood.html")





@permission_required("warehouse.register_delivery")
def finalDelivery(request):
    data = request.POST

    if MyBackend().authenticate(data['username'], data['password']) is not None:
        keys = json.loads(data['keys'])
        Good.objects.filter(pk__in=keys).update(status='U')
        c = {'rlink': '../allgoods/', 'success': "ثبت تحویل کالاها با موفقیت انجام شد"}
        inform_trustee(message=render_to_string('mail/good_needs_label.html', {'keys': keys}),
                    subject='کالاهای نیازمند برچسب‌گذاری')
        return render_to_response("success.html", c)
    else:
        return HttpResponse("borooo")

@permission_required("warehouse.add_new_good")
def orderItemList(request):
    try:
        order = request.POST['order']
        order = Order.objects.get(pk=order)

        category = request.POST['category']
        if category != '':
            category = Category.objects.get(pk=int(category))
        else :
            category = None
    except:
        return HttpResponse('[]')

    orderitems = OrderItem.objects.filter(category=category,order=order,status='P').values('pk','quantity','description')

    result = json.dumps(list(orderitems))

    return HttpResponse(result)

@permission_required("warehouse.view_all_goods")
def allGoodsView(request):
    my_dict = {}
    if request.user.groups.all()[0].name == 'T':
        my_dict.update({'show_receipt': True})
    return render_to_response_wrapper(request, "allGoods.html", my_dict=my_dict)
