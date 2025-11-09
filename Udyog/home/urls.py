# home/urls.py

from django.urls import path, include   # -----> include is needed
from . import views
from .views import (
    MyTokenView,
    NameCreateAPIView, SignupAPIView, LoginAPIView,
    ReferralRequestAPIView, SetRoleView, ProtectedPingView,
    RefererAPIView,                 # -----> you already use this
    ReferralPostListCreate,                # -----> DRF ViewSet we added earlier
    ReferralPostViewSet,
    MeAPIView,
    JobViewSet,
    tracker_stats,
    profile,
    access_denied,
    my_tracker,
    SeekerRequestViewSet
)

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from .views import my_tracker


# ----- DRF Router (API under /api/)



router = DefaultRouter()
router.register(r"referrals", ReferralPostViewSet, basename="referrals")
router.register(r'jobs', JobViewSet, basename='jobs') 
router.register(r"seeker-requests", SeekerRequestViewSet, basename="seeker-requests")




urlpatterns = [
    # ----- Initial pages
    path("", views.landing, name="landing"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("launchpad", views.launchpad, name="launchpad"),

    #common pages
    path("profile", views.profile, name="profile"),
    path("no_token", views.no_token, name="no_token"),
    path("access_denied", views.access_denied, name="access_denied"),


    #test pages
    path("test", views.test, name="test"),
    path("refer", views.referer, name="referer"),
    path("referal_req", views.referal_req, name="referal_req"),
    path("api/me/", MeAPIView.as_view(), name="me"),


    #Seeker Pages
    path("active_referals", views.active_referals, name="active_referals"),
    path("trending", views.trending, name="trending"),
    path("tracker", views.tracker, name="tracker"),


    #referer pages
    path("referer_home", views.referer_home, name="referer_home"),
    path("my_tracker", views.my_tracker, name="my_tracker"),
    
    

    # ----- Auth / small APIs
    path("api/login/", LoginAPIView.as_view(), name="login_api"),
    path("api/signup/", SignupAPIView.as_view(), name="signup_api"),
    path("api/set-role/", SetRoleView.as_view(), name="set_role"),
    path("api/name/", NameCreateAPIView.as_view(), name="name"),
    path("api/referral-request/", ReferralRequestAPIView.as_view(), name="referral_api"),
    path("api/referer/", RefererAPIView.as_view(), name="referer_api"),
    path("api/protected-ping/", ProtectedPingView.as_view(), name="ping"),
    path("api/token/", MyTokenView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/tracker-stats/", tracker_stats, name="tracker_stats"),


    
    # ----- Mount DRF router
   path("api/", include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)