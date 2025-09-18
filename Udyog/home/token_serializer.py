from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = getattr(user,"email",None)
        token['username'] = user.username
        token['Password'] = user.password
        token['role']=getattr(user,"role",None)

        return token
