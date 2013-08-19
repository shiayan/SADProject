# -*- coding: UTF-8 -*-
import json

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from SADProject.myUser import inform_user

from SADProject.myUser.backend import MyBackend
from SADProject.orders.views import changeQuerySet
from SADProject.utils.view_utils import render_to_response_wrapper, jsonListGenerator, deleteFromQuerySet
from SADProject.warehouse.models import Good
from SADProject.damaged.models import Damaged

@permission_required("damaged.view_all_damaged_goods")
def allDamagedView(request):
    return render_to_response_wrapper(request, "alldamaged.html")

@permission_required("damaged.view_all_damaged_goods")
def allDamagedJson(request):
    columns = ["good__pk","good__user","good__category", "status","description"]
    data = Damaged.objects
    return jsonListGenerator(request=request, data=data, columns=columns, template="json/damaged.json")


@permission_required("damaged.view_all_damaged_goods")
def changeDamaged(request):
    columns = ['address', 'status']
    changeQuerySet(request, columns, Damaged.objects)
    return HttpResponse('success')

@permission_required("damaged.view_all_damaged_goods")
def returnDamaged(request):
    columns = ['status']
    damaged = Damaged.objects.get(pk=request.POST['pk'])
    inform_user(user=damaged.good.user, message=render_to_string("mail/damaged_repaired.html", {'good': damaged.good}),
                subject='کالای شما تعمیر شد')
    changeQuerySet(request, columns=columns, queryset=Damaged.objects)
    return HttpResponse('success')

@permission_required("damaged.view_all_damaged_goods")
def deleteDamaged(request):
    damaged = Damaged.objects.get(pk=request.POST['pk'])
    inform_user(user=damaged.good.user, message=render_to_string("mail/damaged_deleted.html", {'good': damaged.good}),
                subject='کالای معیوب شما مرجوعی است')
    deleteFromQuerySet(request, Damaged.objects)
    damaged.good.delete()
    return HttpResponse('success')

###################################
@permission_required("damaged.register_damaged_good_delivery")
def deliverDamagedJson(request):
    columns = ['pk', 'user']
    data = Good.objects.filter(status='D', damaged__status='F')
    my_dict = {'show_user': False, 'checkbox': True, 'show_status': False}
    return jsonListGenerator(request=request, columns=columns, data=data, my_dict=my_dict,
                             template="json/allgoods.json")

@permission_required("damaged.register_damaged_good_delivery")
def deliverDamagedView(request):
    my_dcit = {'delivery_title': 'تحویل کالای تعمیر شده', 'final_delivery_address': '../finaldamageddeliver/',
               'table_json_address': '../json/deliverdamaged', 'show_description': False}
    return render_to_response_wrapper(request, "gooddelivery.html", my_dcit)

@permission_required("damaged.register_damaged_good_delivery")
def finalDamagaedDeliver(request):
    data = request.POST

    if MyBackend().authenticate(data['username'], data['password']) is not None:
        keys = json.loads(data['keys'])
        for key in keys:
            good = Good.objects.get(pk=key)
            damaged = Damaged.objects.get(good=good)
            good.status = damaged.previous_status
            good.save()
            damaged.delete()

        c = {'rlink': '../alldamaged/', 'success': "ثبت تحویل کالاهای تعمیر شده با موفقیت انجام شد"}

        return render_to_response("success.html", c)
    else:
        return HttpResponse("borooo")

######################################33
@permission_required("damaged.add_damaged_good")
def addDamagedView(request):
    my_dcit = {'delivery_title': 'ثبت کالای خراب', 'final_delivery_address': '../finaladd/',
               'table_json_address': '../json/add', 'show_description': True}
    return render_to_response_wrapper(request, "gooddelivery.html", my_dcit)


@permission_required("damaged.add_damaged_good")
def addJson(request):
    columns = ['pk', 'user']
    data = Good.objects.exclude(status='D')
    my_dict = {'show_user': False, 'checkbox': True, 'show_status': False, 'show_description': True}
    return jsonListGenerator(request=request, columns=columns, data=data, my_dict=my_dict,
                             template="json/allgoods.json")


@permission_required("damaged.add_damaged_good")
def finalAdd(request):
    data = request.POST

    if MyBackend().authenticate(data['username'], data['password']) is not None:
        keys = json.loads(data['keys'])
        descriptions = json.loads(data['descriptions'])
        i = 0;
        for key in keys:
            good = Good.objects.get(pk=key)
            Damaged(good=good, previous_status=good.status, description=descriptions[i][0]).save()
            i += 1
        Good.objects.filter(pk__in=keys).update(status='D')
        c = {'rlink': '../alldamaged/', 'success': "ثبت خرابی کالاها با موفقیت انجام شد"}

        return render_to_response("success.html", c)
    else:
        return HttpResponse("borooo")