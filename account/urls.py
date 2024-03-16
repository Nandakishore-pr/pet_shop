from django.urls import path
from account import views

app_name = "account"
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.sign_up,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('signup/otp_verification',views.otp_verification,name='otp_verification'),
    
    
]