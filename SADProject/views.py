'''
Created on Jul 20, 2013

@author: Sina
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render_to_response
from SADProject.utils.view_utils import render_to_response_wrapper

@login_required
def showIndex(request):
    return render_to_response_wrapper(request,"index.html")