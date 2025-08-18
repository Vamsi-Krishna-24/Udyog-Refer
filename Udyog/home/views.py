from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, referal_req, Referer
from .serializers import UserSerializer, Referalrequestserializer, RefererSerializer
from django.shortcuts import redirect, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializer import MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


class NameCreateAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Name saved!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create your views here.
def login(request):
    return render(request, 'home/login.html')


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # authenticate expects the parameter named "username",
        # but it uses your USERNAME_FIELD (email) under the hood.
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # redirect based on role
        if user.role == 'referrer':
            next_path = '/active_referals'
        elif user.role == 'referee':
            next_path = '/referer_home'
        else:
            next_path = '/launchpad'  # role not set yet

        return Response({"redirect": next_path}, status=status.HTTP_200_OK)
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


def referer_home(request):
    return render(request, 'home/referer_home.html')



##There is no Token/ User trying to login without password
def no_token(request):
    return render(request, 'home/no_token.html')

#extra added for authorising

class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    
class ActiveReferralsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected route"})