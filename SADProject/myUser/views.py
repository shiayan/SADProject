# Create your views here.

from django.contrib.auth.models import  User
from django.http import HttpResponse
from SADProject.utils.view_utils import render_to_response_wrapper, jsonListGenerator, deleteFromQuerySet
from django.contrib.auth.decorators import  user_passes_test, permission_required
from SADProject.warehouse.models import Good
from SADProject.myUser.backend import MyBackend

@permission_required("warehouse.register_delivery")
def checkCredentials(request):
    data = request.POST
    if MyBackend().authenticate(data['username'], data['password']) is None:
        return HttpResponse("wrongpass")
    else:
        return HttpResponse("success")

def user_is_superuser(user):
    return  user.is_superuser

@user_passes_test(user_is_superuser)
def usersJson(request,filters={}):
    columns = ['pk', 'username', 'firstname', 'lastname','groups']
    data = User.objects.all()
    return jsonListGenerator(request = request, columns = columns, data = data, template = "json/users.json")

@user_passes_test(user_is_superuser)
def deleteUser(request):
    user = User.objects.get(pk = request.POST['pk'])
    Good.objects.exclude(status = 'D').filter(user = user).update(status = 'W')
    return deleteFromQuerySet(request,User.objects.all())

@user_passes_test(user_is_superuser)
def changeUser(request):
    data = request.POST
    user = User.objects.get(pk=int(data['pk']))
    user.username = data['username']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.groups.clear()
    user.groups.add(int(data['groups']))
    user.save()
    return HttpResponse("success")

@user_passes_test(user_is_superuser)
def addUser(request):
    data = request.POST
    if User.objects.filter(username=data['username']).count() > 0:
        return HttpResponse('error')

    user = User()
    user.username = data['username']
    user.first_name = data['first_name']
    user.email = user.username + '@ce.sharif.edu'
    user.password = "nopassword"
    user.last_name = data['last_name']
    user.save()
    user.groups.add(int(data['groups']))
    user.save()
    return HttpResponse("Response")

@user_passes_test(user_is_superuser)
def usersView(request):
    return render_to_response_wrapper(request,"users.html")