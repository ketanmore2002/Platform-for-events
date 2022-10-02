import razorpay
from traceback import print_tb
from django.shortcuts import render

# Create your views here.


from .models import *

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

RAZOR_KEY_ID = "rzp_test_8IrJ4WuGJAF95Q"
RAZOR_KEY_SECRET = "qxjiUvDTYTccH9AdqGWEAWT5"
razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def pay (request,e,id):
    currency = 'INR'


    if e == "t":

        data = teams.objects.filter(leader_user_id=request.user.id,  leader_user_name=request.user.username,  id=id)

        amount = (int(data[0].fees))*100

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=(int(data[0].fees)*100), currency=currency,payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/paymenthandler/' + "t/" + str(id) + "/"
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

        return render(request, 'pay.html', context=context)


    elif e == "p" :


        data = player.objects.filter(leader_user_id=request.user.id,leader_user_name=request.user.username)

        amount = (int(data[0].fees))*100

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=data[0].fees, currency=currency,payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/' + "p/" + str(request.user.id)
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

        return render(request, 'pay.html', context=context)


 


@csrf_exempt
def paymenthandler(request,e,id):

    if e == "t":

        data = teams.objects.filter(leader_user_id=request.user.id,  leader_user_name=request.user.username,  id=id)

        amount = (int(data[0].fees))*100
 
        # only accept POST request.
        if request.method == "POST":
            try:
            
                # get the required parameters from post request.
                payment_id = request.POST.get('razorpay_payment_id', '')
                razorpay_order_id = request.POST.get('razorpay_order_id', '')
                signature = request.POST.get('razorpay_signature', '')
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
    
                # verify the payment signature.
                result = razorpay_client.utility.verify_payment_signature(params_dict)
                if result is not None:
                    print(result)
            
                    try:
    
                        # capture the payemt
                        x = razorpay_client.payment.capture(payment_id, amount)
    
                        print(x)
                        # render success page on successful caputre of payment
                        # return render(request, 'paymentsuccess.html')

                        if e =="t":
                            teams.objects.filter(id=id).update(payment_status = "paid")
                        elif e == "p" :
                            player.objects.filter(id=id).update(payment_status = "paid")

                        return HttpResponse("paymentsuccess")

                    except:
    
                        # if there is an error while capturing payment.
                        # return render(request, 'paymentfail.html')
                        print(1)
                        return HttpResponse("paymentfail")

                else:
    
                    # if signature verification fails.
                    # return render(request, 'paymentfail.html')
                    print(2)

                    return HttpResponse("paymentfail")

            except:
    
                # if we don't find the required parameters in POST data
                print(3)

                return HttpResponse("paymentfail")
        else:
        # if other than POST request is made.
            print(4)

            return HttpResponse("paymentfail")


    elif  e == "p" :


        data = player.objects.filter(leader_user_id=request.user.id,leader_user_name=request.user.username)

        amount = (int(data[0].fees))*100


        if request.method == "POST":
            try:
            
                # get the required parameters from post request.
                payment_id = request.POST.get('razorpay_payment_id', '')
                razorpay_order_id = request.POST.get('razorpay_order_id', '')
                signature = request.POST.get('razorpay_signature', '')
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
    
                # verify the payment signature.
                result = razorpay_client.utility.verify_payment_signature(params_dict)
                if result is not None:
                    print(result)
                    
                    try:
    
                        # capture the payemt
                        x = razorpay_client.payment.capture(payment_id, amount)
    
                        print(x)
                        # render success page on successful caputre of payment
                        # return render(request, 'paymentsuccess.html')

                        if e =="t":
                            teams.objects.filter(id=id).update(fees = "paid")
                        elif e == "p" :
                            player.objects.filter(id=id).update(fees = "paid")

                        return HttpResponse("paymentsuccess")

                    except:
    
                        # if there is an error while capturing payment.
                        # return render(request, 'paymentfail.html')
                        print(1)
                        return HttpResponse("paymentfail")

                else:
    
                    # if signature verification fails.
                    # return render(request, 'paymentfail.html')
                    print(2)

                    return HttpResponse("paymentfail")

            except:
    
                # if we don't find the required parameters in POST data
                print(3)

                return HttpResponse("paymentfail")
        else:
        # if other than POST request is made.
            print(4)

            return HttpResponse("paymentfail")
