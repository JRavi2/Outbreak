from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('<str:disease>', views.list_hospitals, name='list_hospitals'),
    path('search/', views.search, name='search'),
    path('symptoms/interview/get_info/',views.take_info, name='take_info'),
    path('symptoms/complaints/intialize_interview/', views.inialize_interview, name='initialize_interview'),
    path('symptoms/complaints/initalize_complaints/<str:complaint>', views.initalise_chatbot, name='initialize_chatbot'),
    path('symptoms/complaints/', views.take_symptoms, name='take_symptoms'),
    path('symptoms/confirmation/', views.confirmation, name='confirmation'),
    path('symptoms/interview/<int:age>,<str:sex>', views.interview, name='interview'),
]
