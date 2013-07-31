from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = 'Sina'


def render_to_response_wrapper(request,template):

    c = {}
    c.update(csrf(request))

    return render_to_response(template,c,context_instance=RequestContext(request));


def jsonListGenerator(request,columns,data,template,my_dict = {},default_filters = {}):
    filters = ['__gte','__lte','']
    args = default_filters
    for column in columns:
        for fltr in filters:
            if column + fltr in request.GET:
                args.update({column + fltr : request.GET[column+fltr]})

    data = data.filter(**args).distinct()

    iTotalRecords = data.count()
    iTotalDisplayRecords = data.count()

    if 'iSortCol_0' in request.GET:
        order_str = columns[int(request.GET['iSortCol_0'])]
        if request.GET['sSortDir_0'] == 'desc':
            order_str =  '-' + order_str

        order_arg = []
        order_arg.append(order_str)
        data = data.order_by(*order_arg)

    if 'iDisplayStart' in request.GET:
        iDisplayStart = int(request.GET['iDisplayStart'])
        iDisplayLength =  int(request.GET['iDisplayLength'])
    else:
        iDisplayStart = 0
        iDisplayLength  = iTotalRecords

    iDisplayEnd = min(iDisplayLength + iDisplayStart ,data.count() )
    if 'sEcho' in request.GET:
        sEcho = int(request.GET['sEcho'])
    else:
        sEcho = 1

    if iDisplayLength > 0:
        data = data[iDisplayStart:iDisplayEnd]

    my_dict.update({"objects" : data,'iTotalRecords' : iTotalRecords , 'iTotalDisplayRecords' : iTotalDisplayRecords,'sEcho' : sEcho})
    return render_to_response(template,my_dict,mimetype='application/json')