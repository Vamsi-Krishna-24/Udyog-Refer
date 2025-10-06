from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, referal_req, Referer, Referral_post, SeekerRequest, Referral_post
from .serializers import UserSerializer, Referalrequestserializer, RefererSerializer, ReferralPostSerializer, JobSerializer,SeekerRequestSerializer
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
    queryset = Referral_post.objects.order_by("-created_at")
    serializer_class = ReferralPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['role', 'experience_required', 'location','company_name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)   # attaches logged-in user

    def get_queryset(self):
        qs = Referral_post.objects.order_by("-created_at")
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
class SeekerRequestViewSet(viewsets.ModelViewSet):
    queryset = SeekerRequest.objects.all().order_by("-created_at")
    serializer_class = SeekerRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # get referral post id from request data
        post_id = self.request.data.get("referral_post")
        referral_post = Referral_post.objects.get(id=post_id)

        # prevent self-referrals
        if referral_post.user == self.request.user:
            raise serializers.ValidationError("You cannot request your own referral post.")

        # save with auto-linked users
        serializer.save(
            requester=self.request.user,
            referrer=referral_post.user,
            referral_post=referral_post
        )

    def get_queryset(self):
        user = self.request.user
        # show seeker their own sent requests
        if self.request.query_params.get("view") == "mine":
            return SeekerRequest.objects.filter(requester=user).order_by("-created_at")
        # show referrer all incoming requests
        return SeekerRequest.objects.filter(referrer=user).order_by("-created_at")