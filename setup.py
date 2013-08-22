

__author__ = 'Sina'

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SADProject.settings")

from django.contrib.auth.models import *

# result = ''
# for group in Group.objects.all():
#     result += ',{"name":"' + group.name + '","perms":['
#     miniresult = ""
#     for permission in group.permissions.all():
#         miniresult += '"'  + permission.codename  + '",'
#     miniresult = miniresult[0:-1]  + ']}'
#     result += miniresult
# print result[1:]

def addGroup(name, perms):
    if Group.objects.filter(name=name).count() == 0:
        group = Group(name=name)
        group.save()
    else:
        group = Group.objects.get(name=name)

    for perm in perms:
        permission = Permission.objects.get(codename=perm)
        group.permissions.add(permission)
    group.save()


groups = [{"name": "A",
           "perms": ["change_user", "add_new_order", "view_accepted_orders", "view_all_orders", "view_buy_orders",
                     "view_my_orders", "view_unviewed_orders", "add_new_good", "add_receipt", "change_categories",
                     "register_delivery", "view_all_goods"]}, {"name": "S", "perms": ["add_damaged_good",
                                                                                      "register_damaged_good_delivery",
                                                                                      "view_all_damaged_goods",
                                                                                      "add_new_order",
                                                                                      "view_accepted_orders",
                                                                                      "view_my_orders", "add_category",
                                                                                      "add_new_good", "add_receipt",
                                                                                      "change_categories",
                                                                                      "register_delivery",
                                                                                      "view_all_goods",
                                                                                      "view_my_goods"]},
          {"name": "T", "perms": ["add_new_order", "view_my_orders", "add_receipt", "view_all_goods", "view_my_goods"]},
          {"name": "B", "perms": ["add_new_order", "view_buy_orders", "view_my_orders", "view_my_goods"]},
          {"name": "U", "perms": ["add_new_order", "view_my_orders", "view_my_goods"]}
]
for group in groups:
    addGroup(group['name'],group['perms'])
for user in User.objects.all():
    if user.is_superuser:
        user.groups.add ( Group.objects.get(name ='A'))
        user.save()
    else:

        if user.groups.all().count() ==0:
            user.groups.add ( Group.objects.get(name ='U'))
            user.save()

