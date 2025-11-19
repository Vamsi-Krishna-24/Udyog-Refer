from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from .models import User, referal_req, Referer, Referral_post, SeekerRequest, Referral_post
from .serializers import (UserSerializer,
                        Referalrequestserializer, 
                        RefererSerializer,
                        ReferralPostSerializer, 
                        JobSerializer,
                        SeekerRequestSerializer,
                        ProfileSerializer)
from .permissions import IsReferrerOnCreate
from django.shortcuts import redirect, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .token_serializer import MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import viewsets
from .models import Job
from .serializers import JobSerializer
from rest_framework import viewsets, filters, serializers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.pagination import PageNumberPagination
from home.models import SeekerRequest
from .models import Profile
from django.shortcuts import redirect
from django.conf import settings
import requests
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password






class NameCreateAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Name saved!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def landing(request):
    return render(request, 'home/landing.html')

def profile(request):
    return render(request, 'home/profile.html')

def my_profile(request):
    return render(request, 'home/my_profile.html')


# Create your views here.
def login(request):
    return render(request, 'home/login.html')

# views.py
@api_view(['GET'])
def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("/login")

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:8000/api/google/callback/",
        "grant_type": "authorization_code",
    }

    token_resp = requests.post("https://oauth2.googleapis.com/token", data=token_data).json()
    google_access = token_resp.get("access_token")
    if not google_access:
        return redirect("/no_token")

    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {google_access}"}
    ).json()

    email = userinfo.get("email")
    name = userinfo.get("name", email.split("@")[0])

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": name,
            "password": make_password(get_random_string(12)),
        }
    )

    # create tokens
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    # save session
    auth_login(request, user)

    # prepare redirect based on role
    if user.role == "referrer":
        redirect_url = "/referer_home"
    elif user.role == "referee":
        redirect_url = "/active_referals"
    else:
        redirect_url = "/launchpad"

    # Instead of redirecting immediately → return tokens as query
    return redirect(f"{redirect_url}?access={access}&refresh={refresh}&email={email}&role={user.role}")
class LoginAPIView(APIView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        # -----> mint tokens + add custom claims
        refresh = RefreshToken.for_user(user)
        refresh['role'] = getattr(user, 'role', None)   # -----> custom claim
        refresh['email'] = getattr(user, 'email', None)

        # -----> correct redirect by role
        if user.role == 'referrer':
            next_path = '/referer_home'
        elif user.role == 'referee':
            next_path = '/active_referals'
        else:
            next_path = '/launchpad'

        return Response({
    "redirect": next_path,
    "access": str(refresh.access_token),
    "refresh": str(refresh),
    "role": user.role,
    "email": user.email,
    "username": user.username,
    "id": user.id
    
}, status=200)
class ReferralRequestAPIView(APIView):
    def post(self, request):
        serializer = Referalrequestserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Referral data saved!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RefererAPIView(APIView):
    def post(self,request):
        serializer = RefererSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Referer data saved!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    

def signup(request):
    return render(request, 'home/signup.html')


class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user_id": user.id,
                "email":user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def launchpad(request):
    return render(request, 'home/launchpad.html')


class SetRoleView(APIView):
    # permission_classes = [permissions.IsAuthenticated]  # -----> REMOVE for now

    def post(self, request):
        role = (request.data.get("role") or "").strip().lower()
        user_id = request.data.get("user_id")  # -----> coming from localStorage
        email = request.data.get("email")

        valid_values = {User.ROLE_REFERRER, User.ROLE_REFEREE}
        if role not in valid_values:
            return Response({"error": "role must be 'referrer' or 'referee'"},
                            status=status.HTTP_400_BAD_REQUEST)

        # -----> fetch the correct user explicitly
        if user_id:
            user = get_object_or_404(User, id=user_id)
        elif email:
            user = get_object_or_404(User, email=email)
        else:
            return Response({"error": "Provide user_id or email"},
                            status=status.HTTP_400_BAD_REQUEST)

        # -----> update & persist
        user.role = role
        user.save(update_fields=["role"])

        # -----> tell frontend where to go next
        redirect_path = "/referer_home" if role == User.ROLE_REFERRER else "/active_referals"
        return Response({"ok": True, "role": role, "redirect": redirect_path},
                        status=status.HTTP_200_OK)


def test(request):
    return render(request, 'home/test.html')

def referer(request):
    return render(request, 'home/referer.html')


def referal_req(request):
    return render(request, 'home/referal_req.html')

def active_referals(request):
    return render(request, 'home/active_referals.html')



class ProtectedPingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "Token is valid"})


def trending(request):
    return render(request, 'home/trending.html')

def tracker(request):
    return render(request, 'home/tracker.html')


def my_tracker(request):
    return render(request, 'home/my_tracker.html')

def referer_home(request):
    return render(request, 'home/referer_home.html')



##There is no Token/ User trying to login without password
def no_token(request):
    return render(request, 'home/no_token.html')

def access_denied(request):
    return render(request, "home/access_denied.html")


#extra added for authorising

class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    
class ActiveReferralsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected route"})
    


# defining a class so that when Referer posts then that will hit up in the screen of Referer
class ReferralPostListCreate(APIView):               # ///// /api/referrals/ (GET, POST)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Referral_post.objects.select_related("referrer").order_by("-created_at")
        data = ReferralPostSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # only referrers can create
        if getattr(request.user, "role", "").lower() != "referrer":
            return Response({"detail": "Only referrers can post."},
                            status=status.HTTP_403_FORBIDDEN)

        ser = ReferralPostSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        obj = ser.save(referrer=request.user)        # ///// attach logged-in user
        return Response(ReferralPostSerializer(obj).data,
                        status=status.HTTP_201_CREATED)



class ReferralPostViewSet(viewsets.ModelViewSet):
    serializer_class = ReferralPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['role', 'experience_required', 'location', 'company_name']

    def get_queryset(self):
        user = self.request.user

        # 🧠 Step 1 — Base queryset
        if user.role == "referrer":
            qs = Referral_post.objects.filter(user=user).order_by("-created_at")
        else:
            qs = Referral_post.objects.all().order_by("-created_at")

        # 🧠 Step 2 — Apply search filters (if provided)
        role = self.request.query_params.get("role")
        exp = self.request.query_params.get("experience")
        loc = self.request.query_params.get("location")
        comp = self.request.query_params.get("company")

        if role:
            qs = qs.filter(role__icontains=role)
        if exp:
            qs = qs.filter(experience_required__icontains=exp)
        if loc:
            qs = qs.filter(location__icontains=loc)
        if comp:
            qs = qs.filter(company_name__icontains=comp)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)






##TEST View to check passage of user role back to server
class MeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "email": getattr(u, "email", None),
            "role": getattr(u, "role", None),   # -----> your custom field
            "is_staff": getattr(u, "is_staff", False),
        })
    
class JobViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["company", "position", "location", "description"]

    def get_queryset(self):
        qs = Job.objects.order_by("-published_at", "-created_at")
        loc = self.request.query_params.get("location")
        if loc:
            qs = qs.filter(location__icontains=loc)
        return qs


#API View for Seeker Request
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets, permissions, serializers
from .models import SeekerRequest, Referral_post
from .serializers import SeekerRequestSerializer


#API View for Seeker Request
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import SeekerRequest, Referral_post
from .serializers import SeekerRequestSerializer


class SeekerRequestViewSet(viewsets.ModelViewSet):
    queryset = SeekerRequest.objects.all().order_by("-created_at")
    serializer_class = SeekerRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get("referral_post")
        referral_post = Referral_post.objects.get(id=post_id)

        if referral_post.user == self.request.user:
            raise serializers.ValidationError("You cannot request your own referral post.")

        serializer.save(
            requester=self.request.user,
            referrer=referral_post.user,
            referral_post=referral_post
        )

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        seeker_request = self.get_object()
        if seeker_request.status != "PENDING":
            return Response({"detail": "Already finalized."},
                            status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get("reason", "").strip()
        seeker_request.status = "ACCEPTED"
        if reason:
            seeker_request.reason = reason
        seeker_request.save()
        return Response({"status": "accepted"})


    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        seeker_request = self.get_object()
        if seeker_request.status != "PENDING":
            return Response({"detail": "Already finalized."},
                            status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get("reason", "").strip()
        seeker_request.status = "REJECTED"
        seeker_request.reason = reason
        seeker_request.save()
        return Response({"status": "rejected"})

# Getting the Stats of the user for Tracker Page

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tracker_stats(request):
    user = request.user
    # count how many applications this user sent
    apps_sent = SeekerRequest.objects.filter(requester_id=user.id).count()
    return Response({"applications_sent": apps_sent})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def referer_tracker_stats(request):
    user = request.user

    # A. Refers posted
    refers_posted = Referral_post.objects.filter(user_id=user.id).count()

    # B. Referral updates (requests received by this referer)
    referral_updates = SeekerRequest.objects.filter(referrer_id=user.id).count()

    return Response({
        "refers_posted": refers_posted,
        "referral_updates": referral_updates
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def tracker_stats(request):
    user = request.user

    # total applications sent by this seeker
    apps_sent = SeekerRequest.objects.filter(requester_id=user.id).count()

    # total referrals with status ACCEPTED or REJECTED
    status_updates = SeekerRequest.objects.filter(
        requester_id=user.id,
        status__in=["ACCEPTED", "REJECTED"]
    ).count()

    return Response({
        "applications_sent": apps_sent,
        "status_updates": status_updates
    })


#API Profile Viewset


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle Profile CRUD operations for the logged-in user.
    - GET → fetch current user's profile
    - PUT/PATCH → update profile
    - POST → create profile (auto-links to user)
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Each user can only access their own profile
        return Profile.objects.filter(user=self.request.user)
    
    def get_object(self):
        return Profile.objects.get_or_create(user=self.request.user)[0]


    def list(self, request, *args, **kwargs):
        """
        GET /api/profile/ → returns the current user's profile
        """
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        POST /api/profile/ → only allowed once (creates if missing)
        """
        if Profile.objects.filter(user=request.user).exists():
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        PUT /api/profile/ → update the current user's profile
        """
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /api/profile/ → partial update for current user's profile
        """
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

