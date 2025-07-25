from django.urls import path
from . import views
from django.urls import path
from .views import NameCreateAPIView, SignupAPIView, LoginAPIView

urlpatterns = [
    path('',views.login,name='login'), 
    path('login/',views.login,name='login/'), 
    path('api/login/', LoginAPIView.as_view(), name='login_api'),
    path('api/signup/', SignupAPIView.as_view(), name='signup_api'),
    path('signup',views.signup,name='signup'), 
    path('launchpad/',views.launchpad,name='launchpad'), 
    path('test',views.test,name='test'),
    path('api/name/', NameCreateAPIView.as_view(), name='name'),
    path('refer', views.referer, name='referer'),
    path('referal_req', views.referal_req, name='referal_req'),
    path('active_referals',views.active_referals,name='active_referals'), 
    path('trending',views.trending,name='trending'),
    path('tracker',views.tracker,name='tracker'), 
]

