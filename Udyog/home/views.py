from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User


from .serializers import UserSerializer
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializer import MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

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
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            # Login successful → redirect
            return Response({"redirect": "/active_referals"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def signup(request):
    return render(request, 'home/signup.html')

class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def launchpad(request):
    return render(request, 'home/launchpad.html')

def test(request):
    return render(request, 'home/test.html')

def referer(request):
    return render(request, 'home/referer.html')


def referal_req(request):
    return render(request, 'home/referal_req.html')

def active_referals(request):
    return render(request, 'home/active_referals.html')


def trending(request):
    return render(request, 'home/trending.html')

def tracker(request):
    return render(request, 'home/tracker.html')





#extra added for authorising

class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    
class ActiveReferralsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected route"})