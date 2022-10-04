"""event URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from django.urls.conf import include
from team import views

urlpatterns = [
    path("pay/<str:e>/<int:id>/<str:event_id>/",views.pay,name='pay'),
    path('paymenthandler/<str:e>/<int:id>/<str:event_id>/', views.paymenthandler, name='paymenthandler'),

    # path("order_page/<str:e>/<int:id>/",views.order_page,name='order_page'),
    # path("handlerequest/<str:e>/<int:id>/", views.handlerequest, name='handlerequest'),

    path("",views.index,name='index'),
    path("adminpanel/<int:id>/",views.adminpanel,name='adminpanel'),
    path("check_event/",views.check_event,name='check_event'),

    path("participants_details/",views.participants_details,name='participants_details'),
    path("participation_form/<int:id>/",views.participation_form,name='participation_form'),
    # path("ev/",views.register_option,name='register_option'),

    path("api_events_id/<int:id>/", views.api_events_id, name="api_events_id"),
    path("api_teams/",views.api_teams,name='api_teams'),
    path("api_players/",views.api_players,name='api_players'),
    path("single_team/<str:team_id>/",views.single_team,name='single_team'),
    path("single_player/<str:player_id>/",views.single_player,name='single_player'),
    path("api_events/",views.api_events,name='api_events'),
    path("unpaid_data_number/<int:number>/", views.unpaid_data_number, name="unpaid_data_number"),


    path("cout_data/", views.cout_data, name="cout_data"),
    path("data_number/<int:number>/", views.data_number, name="data_number"),

    path("unpaid_cout_data/", views.unpaid_cout_data, name="unpaid_cout_data"),

    path("add_event/", views.add_event, name="add_event"),
    path("events/", views.event_info, name="events"),
    path("events/details/", views.event_details, name="event_details"), 


    path("add_team/", views.add_Team, name="add_team"), 
    path("add_participant/", views.add_Participant, name="add_participant"),

    path("my_events/", views.my_events, name="my_events"),
    path("about/", views.about_view, name="about"),
    path("logout/", views.logout_view, name="logout"),
    path("details/<int:id>/", views.details_view, name="details_view"), 
    path("become_host/", views.become_host, name="become_host"),
    path("temp_login/", views.temp_login, name="temp_login"),
    path("delete_event/<int:id>/", views.delete_event, name="delete_event"),
    path("csv/player/", views.getfile_player, name="getfile_player"),
    path("csv/teams/", views.getfile_team, name="getfile_team"),
   
]
