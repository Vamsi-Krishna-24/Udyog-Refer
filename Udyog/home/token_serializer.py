from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['role'] = user.role
        token['id'] = str(user.id)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['username'] = self.user.username
        data['role'] = self.user.role      
        data['id'] = self.user.id  
        return data
