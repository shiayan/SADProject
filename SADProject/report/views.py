from django.template.loader import render_to_string
from SADProject.damaged.models import Damaged
from SADProject.orders.models import Order
from SADProject.settings import BASE_DIR
import jdatetime
from datetime import datetime
import os
from SADProject.warehouse.models import Good

__author__ = 'Sina'
from django.http import HttpResponse
def orderReportView(request):
    columns = ["pk","user","submitDate", "status"]
    data = Order.objects
    return pdfGenerator(request,columns,data,'reports/order.html')
def damagedReportView(request):
    columns = ["good__pk","good__user","good__category", "status","description"]
    data = Damaged.objects
    return pdfGenerator(request,columns,data,'reports/damaged.html')
def goodReportView(request):
    columns = ['pk', 'user', 'category', 'submitDate', 'status']
    data = Good.objects
    return pdfGenerator(request,columns,data,'reports/goods.html')
def pdfGenerator(request,columns,data,template,my_dict = {},default_filters = {}):
    filters = ['__gte','__lte','']
    args = {}
    args.update(default_filters)

    for column in columns:
        for fltr in filters:
            if column + fltr in request.GET:
                if request.GET[column+fltr] != '':
                    args.update({column + fltr : request.GET[column+fltr]})


    data = data.filter(**args).distinct()

    iTotalRecords = data.count()


    if 'iSortCol_0' in request.GET:
        order_str = columns[int(request.GET['iSortCol_0'])]
        if request.GET['sSortDir_0'] == 'desc':
            order_str =  '-' + order_str

        order_arg = []
        order_arg.append(order_str)
        data = data.order_by(*order_arg)



    my_dict.update({"objects" : data,'iTotalRecords' : iTotalRecords,'today' : jdatetime.datetime.now().strftime('%d-%m-%Y')})

    html = render_to_string(template,my_dict)
    html_file = open(os.path.join(BASE_DIR,'../' + str(datetime.now().microsecond) + '.html'),'w')
    html_file.write(html.encode('UTF-8'))
    html_file.flush()
    html_file.close()

    os.system("wkhtmltopdf " + html_file.name + " " +  html_file.name[:-4] + "pdf" )
    pdf_file =  open( html_file.name[:-4] + 'pdf' , 'rb')
    pdf_data = pdf_file.read()
    pdf_file.close()
    os.remove(pdf_file.name)
    os.remove(html_file.name)
    response = HttpResponse(pdf_data, content_type='application/vnd.pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response



