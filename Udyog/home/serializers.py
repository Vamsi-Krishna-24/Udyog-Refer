from rest_framework import serializers
from .models import User, ReferralReq, Referrer

# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']  # order doesn’t matter
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False, 'allow_null': True}  # -----> key line
        }

    def create(self, validated_data):
        # -----> don’t require role at signup
        role = validated_data.pop('role', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, role=role, **validated_data)
        return user
    
class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']
        

    
class Referralrequestserializer(serializers.ModelSerializer):
        class Meta:
            model= ReferralReq
            fields = '__all__'

class RefererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referrer
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
        



        