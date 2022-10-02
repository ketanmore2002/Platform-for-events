from traceback import print_tb
from django.shortcuts import render

# Create your views here.


from .models import *

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required





# --------------------------------------------------------------------------------------------------------------------------------------------------------





from paytm import Checksum

MERCHANT_ID = "ISaUZX44618363435046"
MERCHANT_KEY = "l4hosyu56h8kd4DN"

@csrf_exempt
@login_required(login_url='/')
def pay(request,e,id):

    if e == "t":

        orders_placed = teams.objects.get(id=id)     

        param_dict = {

            'MID': MERCHANT_ID,
            'ORDER_ID': str(1008),
            'TXN_AMOUNT': str(orders_placed.fees),
            'CUST_ID': str(request.user.id),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/paymenthandler/' + str(e) + str("/") + str(orders_placed.id) + str("/"),
            

        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        
        return render(request, 'paytm.html', {'param_dict': param_dict})


    

    elif e == "p" :

        orders_placed = player.objects.get(id=id)     

        param_dict = {

            'MID': MERCHANT_ID,
            'ORDER_ID': str(orders_placed.id),
            'TXN_AMOUNT': str(orders_placed.fees),
            'CUST_ID': str(request.user.id),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/paymenthandler/'  + str(e) + str("/") + str(orders_placed.id) + str("/"),
            

        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        
        return render(request, 'paytm.html', {'param_dict': param_dict})






@csrf_exempt
def paymenthandler(request, e, id):

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)

    if verify:
        print(1)
        if response_dict['RESPCODE'] == '01':
            print(2)

            if e == "t" :
            
                teams.objects.filter(id=id).update(payment_status="paid")

            elif e == "p" :

                player.objects.filter(id=id).update(payment_status="paid")
            
            # return render(request, 'order_successful.html', {'id': id})
            return HttpResponse(True)
        else:
            # return render(request, 'order_fail_page.html')
            return HttpResponse(False)
    
    # return render(request, 'order_fail_page.html')
    return HttpResponse(False)

    


    

# --------------------------------------------------------------------------------------------------------------------------------------------------------
