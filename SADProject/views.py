'''
Created on Jul 20, 2013

@author: Sina
'''
from django.shortcuts import  render_to_response
def showIndex(request):
    return render_to_response("index.html",locals())