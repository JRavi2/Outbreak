from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('list_hospital/',include('list_hospital.urls'), name='home'),
    path('accounts/', include('accounts.urls')),
]
