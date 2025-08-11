from django.urls import path
from . import views
from django.urls import path
from .views import ActiveReferralsView
from .views import MyTokenView
from .views import NameCreateAPIView, SignupAPIView, LoginAPIView, ReferralRequestAPIView, SetUserRoleAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('',views.login,name='login'), 
    path('api/login/', LoginAPIView.as_view(), name='login_api'),
    path('api/signup/', SignupAPIView.as_view(), name='signup_api'),
    path('signup',views.signup,name='signup'), 
    path('api/active-referrals/', ActiveReferralsView.as_view(), name='active_referrals_api'),  # -----> NEW
    path('launchpad',views.launchpad,name='launchpad'), 
    path('test',views.test,name='test'),
    path('api/name/', NameCreateAPIView.as_view(), name='name'),
    path('referer', views.Referrer, name='referer'),
    path('referal_req', views.ReferralReq, name='referal_req'),
    path('active_referals',views.active_referals,name='active_referals'), 
    path('trending',views.trending,name='trending'),
    path('tracker',views.tracker,name='tracker'), 
    path('referer_home',views.referer_home,name='referer_home'),
    path('api/token/', MyTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/referral-request/', ReferralRequestAPIView.as_view(), name='referral_api'),
    path('api/referer/', views.RefererAPIView.as_view(), name='referer_api'),
    path('api/set-role/', SetUserRoleAPIView.as_view(), name='set_role_api'),
]

