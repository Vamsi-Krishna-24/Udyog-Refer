from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Name
from .serializers import NameSerializer

class NameCreateAPIView(APIView):
    def post(self, request):
        serializer = NameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Name saved!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
def login(request):
    return render(request, 'home/login.html')

def signup(request):
    return render(request, 'home/signup.html')

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
