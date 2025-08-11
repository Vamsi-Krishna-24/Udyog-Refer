from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, ReferralReq, Referrer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, Referralrequestserializer, RefererSerializer
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializer import MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import RoleUpdateSerializer


user = User.objects.create_user(...)



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
        username = request.data.get("username")  # -----> now this is the actual username
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # -----> decide redirect by role
        if user.role == 'referrer':     # ///// must match your model’s stored value
            next_path = '/referer_home'
        elif user.role == 'referee':
            next_path = '/active_referals'  # ///// keep your current spelling
        else:
            next_path = '/launchpad'    # ///// role is null → send to choose role

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "redirect": next_path
        }, status=status.HTTP_200_OK)




class ReferralRequestAPIView(APIView):
    def post(self, request):
        serializer = Referralrequestserializer(data=request.data)
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
            serializer.save()   
            return Response({
                "message": "User created successfully",
                "user_id":user.id,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SetUserRoleAPIView(APIView):
    """
    POST payload options:
    - { "user_id": 123, "role": "referrer" }   -----> prefer this
    - or { "email": "user@example.com", "role": "referrer" }  -----> fallback if you don’t have id
    """

    def post(self, request):
        # read identifiers
        user_id = request.data.get('user_id')      # -----> pass this from launchpad
        email = request.data.get('email')          # -----> only if you don’t have id
        role_value = request.data.get('role')

        # fetch user
        if user_id:
            user = get_object_or_404(User, id=user_id)
        elif email:
            user = get_object_or_404(User, email=email)
        else:
            return Response({"error": "Provide user_id or email"}, status=status.HTTP_400_BAD_REQUEST)

        # validate & update only the role
        ser = RoleUpdateSerializer(instance=user, data={"role": role_value}, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        ser.save()
        return Response(
            {"message": "Role updated", "role": ser.data["role"]},
            status=status.HTTP_200_OK
        )

def launchpad(request):
    return render(request, 'home/launchpad.html')

def test(request):
    return render(request, 'home/test.html')

def Referrer(request):
    return render(request, 'home/referer.html')


def ReferralReq(request):
    return render(request, 'home/referal_req.html')

def active_referals(request):
    return render(request, 'home/active_referals.html')


def trending(request):
    return render(request, 'home/trending.html')

def tracker(request):
    return render(request, 'home/tracker.html')


def referer_home(request):
    return render(request, 'home/referer_home.html')

class ActiveReferralsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "This is a protected route"})





#extra added for authorising

class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

