from django.urls import path
from BLMApp import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.homePage, name='home'),
    path('home/', views.homePage, name='home'),
    path('form/', views.loanForm, name='loanForm'),
    path('availLoans/', views.availLoans, name='availableLoans'),
    path('kycRegistration/', views.kycDatas, name='kycRegistrationForm'),
    path('yourLoans/', views.yourLoans, name='yourLoans'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='BLMApp/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('loanConfirmation/', views.loanConfirmation, name='loanConfirmation'),
    path('payEmi/', views.payEmi, name='payEmi'),
    path('paymentPage/', views.paymentPage, name='paymentPage'),    
    path('loanSuccess/', views.loanSuccess, name='loanSuccess'),    
    path('paymentSuccess/', views.paymentSuccess, name='paymentSuccess'),    
]