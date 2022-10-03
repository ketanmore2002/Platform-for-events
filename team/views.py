from traceback import print_tb
from django.shortcuts import render

# from event import team

# Create your views here.


from .models import *

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.core import serializers

from .forms import *

from django.shortcuts import redirect





# --------------------------------------------------------------------------------------------------------------------------------------------------------





from paytm import Checksum

MERCHANT_ID = "ISaUZX44618363435046"
MERCHANT_KEY = "l4hosyu56h8kd4DN"

@csrf_exempt
@login_required(login_url='/')
def pay(request,e,id,event_id):


    if e == "t":
        
        amount = events.objects.filter(id = event_id)[0].event_fee

        orders_placed = teams.objects.get(id=id)     

        param_dict = {

            'MID': MERCHANT_ID,
            'ORDER_ID': str(orders_placed.id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(request.user.id),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/paymenthandler/' + str(e) + str("/") + str(orders_placed.id) + str("/") + str(event_id) + str("/"),
            

        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        
        return render(request, 'paytm.html', {'param_dict': param_dict})


    

    elif e == "p" :

        amount = events.objects.filter(id = event_id)[0].event_fee

        orders_placed = player.objects.get(id=id)     

        param_dict = {

            'MID': MERCHANT_ID,
            'ORDER_ID': str(orders_placed.id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(request.user.id),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/paymenthandler/'  + str(e) + str("/") + str(orders_placed.id) + str("/") + str(event_id) + str("/"),
            

        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        
        return render(request, 'paytm.html', {'param_dict': param_dict})






@csrf_exempt
def paymenthandler(request, e, id, event_id) :

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


def index (request):
    competitions = events.objects.all()
    return render (request , 'landing_page.html', {"events": competitions})
    
from django.db.models import Sum
@login_required(login_url='/')
def adminpanel (request,id) :

    user_name =  request.user.username
    user_id =  request.user.id
    # total_users = teams.objects.all().count() + player.objects.all().count()
    total_users = player.objects.all().count() + teams.objects.aggregate(Sum('number_of_members'))["number_of_members__sum"]



    if host.objects.filter(user_name = user_name , user_id = user_id , status = "active").exists() :

        if events.objects.filter(id=id,host_user_name = user_name , host_user_id = user_id).exists() :

            event = events.objects.get(id=id,host_user_name = user_name , host_user_id = user_id)
            event_name = event.event_name
            event_desc = event.discription
            event_type = event.type_of_event

    

            if event.type_of_event == "Team":
                data = teams.objects.all().filter(event_id = id, event_participated = event_name ,payment_status="paid")[::-1]
                current_event_paticipants = len(data)
                unpaid_data = teams.objects.all().filter(event_id = id,event_participated = event_name, payment_status="unpaid")[::-1]
                current_event_paticipants_unpaid = len(unpaid_data)
            else:
                data = player.objects.all().filter(payment_status="paid")[::-1]
                current_event_paticipants = len(data)
                unpaid_data = player.objects.all().filter(payment_status="unpaid")[::-1]
                current_event_paticipants_unpaid = len(unpaid_data)

            total_amount = current_event_paticipants * event.event_fee

    return render (request, 'adminpanel.html', {"data": data, "unpaid_data": unpaid_data, "event_name": event_name, "event_desc": event_desc, "event_type": event_type, "total_users": total_users, "event_paid_participant": current_event_paticipants, "total_amount": total_amount, "unpaid_users": current_event_paticipants_unpaid})

def check_event (request):
    userID = request.user.id
    data = events.objects.all().filter(host_user_id=str(userID))
    return render (request,'check_event.html', {"events": data})


@login_required(login_url='/')
def add_event(request):
    form = eventsForm(request.POST or None)
    if form.is_valid():
        form.save()
    userID = request.user.id
    data = events.objects.all().filter(host_user_id=str(userID))
    return render (request,'check_event.html', {"events": data})



@login_required(login_url='/')
def my_events(request):
    id = request.user.id
    name = request.user.username
    email = request.user.email
    obj = events.objects.all().filter(host_user_name=name, host_user_id=id).exists()
    if obj:
        return redirect("/check_event/")
    
    eventlist = events.objects.all().filter(host_user_id = id)
    return render(request, "my_events.html", {"events": eventlist})



@login_required(login_url='/')
def add_Team(request):
    if request.method == "POST":
        # request.POST['number_of_members'] = int()
        form = teamsForm(request.POST or None)
        print(form)
        if form.is_valid():
            obj = form.save()
            return redirect("/pay/" +"t/" + str(obj.id) + "/" + str(obj.event_id) + "/")
        else:
            return HttpResponse('Something Went Wrong!!!')


@login_required(login_url='/')
def add_Participant(request):
    if request.method == "POST":
        form = playerForm(request.POST or None)
        if form.is_valid():
            obj = form.save()
            return redirect("/pay/" +"p/" + str(obj.id) + "/" + str(obj.event_id) + "/")


@login_required(login_url='/')
def dashboard (request):

    return render (request,'dashboard.html')


@login_required(login_url='/')
def participants_details (request):
    
    return render (request , 'participants_details.html')
    

def participation_form (request,id) :
    data = events.objects.filter(id=id)[0]
    return render (request, 'participation_form.html', {"event": data})
    
     

@login_required(login_url='/')
def register_option (request):
    return render (request,'register_option.html')

@login_required(login_url='/')
def api_teams (request):
    data = teams.objects.all()
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')

@login_required(login_url='/')
def api_players (request):
    data = player.objects.all()
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')

@login_required(login_url='/')
def single_team (request, team_id):
    data = teams.objects.all().filter(id=team_id)
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')

@login_required(login_url='/')
def single_player (request, player_id):
    data = player.objects.all().filter(id= player_id)
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')



@login_required(login_url='/')
def api_events (request):
    data = events.objects.all()
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')


@login_required(login_url='/')
def api_events_id (request,id):
    data = events.objects.filter(id = id)
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')




@login_required(login_url='/')
def event_info (request):
    data = events.objects.all()
    return render (request,'register_option.html', {"events": data})


@login_required(login_url='/')
def event_details (request):
    data = events.objects.filter(host_user_name = request.user.username , host_user_id = request.user.id)
    return render (request,'event_detail.html')



@login_required(login_url='/')
def cout_data (request):
    obj = teams.objects.all().filter(payment_status="paid").count()
    return HttpResponse(obj)


@login_required(login_url='/')
def data_number (request, number):
    # num = request.POST["num"]
    data = teams.objects.all().filter(payment_status="paid").order_by("-id")[:number][::-1]
    # data = Agreement_Orders.objects.all().filter(payment_status="paid")[:number]
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')



@login_required(login_url='/')
def unpaid_cout_data (request):
    obj = teams.objects.all().filter(payment_status="unpaid").count()
    return HttpResponse(obj)


@login_required(login_url='/')
def unpaid_data_number (request, number):
    data = teams.objects.all().filter(payment_status="unpaid").order_by("-id")[:number][::-1]
    qs_json = serializers.serialize('json', data)
    return HttpResponse(qs_json, content_type='application/json')


from django.contrib.auth import logout

@login_required(login_url='/')  # redirect when user is not logged in
def logout_view(request):

    logout(request)
    return redirect('/')

def about_view(request):
    return render(request, "about.html")



def details_view (request,id) :    
    data = events.objects.filter(id=id)[0]
    return render (request, "details.html" ,{"event" : data})


@login_required(login_url='/')
def become_host(request):
    # user_name =  request.user.username
    # user_id =  request.user.id
    # if host.objects.filter(user_name = user_name , user_id = user_id , status = "active").exists() or host.objects.filter(user_name = user_name , user_id = user_id , status = "deactive").exists():

    #     return redirect("/check_event")

    # else :

    #     host.objects.create(user_name = user_name , user_id = user_id , status = "deactive")
        return render(request , 'host.html')
    