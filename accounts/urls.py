from django.urls import path
from django.contrib.auth import views as djViews
from . import views

urlpatterns = [
    path('login/', djViews.LoginView.as_view(
        template_name='accounts/signIn.html'), name='login'),
    path('logout/', djViews.LogoutView.as_view(), name='logout'),
    path('signup/patient/', views.signup_p, name='signup_p'),
    path('signup/hospital/', views.signup_h, name='signup_h'),
    path('pat/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('hos/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('hos/upd-tokens/', views.update_tokens, name='update_tokens'),
    path('hos/upd-tokens/incr-tokens/<str:dept>/', views.increase_tokens, name='increase_tokens'),
    path('hos/upd-tokens/decr-tokens/<str:dept>/', views.decrease_tokens, name='decrease_tokens'),
]
