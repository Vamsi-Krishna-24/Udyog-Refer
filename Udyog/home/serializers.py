from rest_framework import serializers
from .models import User, referal_req, Referer

# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True} 
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user
    
class Referalrequestserializer(serializers.ModelSerializer):
        class Meta:
            model= referal_req
            fields = '__all__'

class RefererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referer
        fields = ['company_name', 'your_role', 'first_name', 'middle_name', 'last_name', 
                  'phone_number', 'mail_id', 'linkedin_url', 'github_url', 'bio']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'mail_id': {'required': True},
            'linkedin_url': {'required': True},
            'github_url': {'required': True},
            'bio': {'required': True}
        }
        



        