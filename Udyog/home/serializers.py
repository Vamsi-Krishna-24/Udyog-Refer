from rest_framework import serializers
from .models import User, referal_req, Referer, Referral_post, Job
from rest_framework import serializers
from .models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.timesince import timesince



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
        


## Creating another serializer for posting REFERRAL in DB 

class ReferralPostSerializer(serializers.ModelSerializer):
    referrer_name = serializers.CharField(source="user.username", read_only=True)
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Referral_post   # ✅ match your model class name
        fields = [
            "id",
            "company_name",
            "role",                  # fixed lowercase
            "referral_domains",      # fixed typo
            "job_description",
            "experience_required",
            "availability",
            "location",
            "salary_expectation",
            "link_to_apply",
            "created_at",
            "referrer_name", 
            "time_since",           
        ]

    def get_time_since(self, obj):
        return timesince(obj.created_at) + " ago"

          
class JobSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="position")                 # UI expects title
    apply_url = serializers.URLField(source="url", read_only=True)   # UI expects apply_url
    description_short = serializers.SerializerMethodField()
    posted_ago = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id",
            "title", "company", "location",
            "description", "description_short",
            "salary",
            "apply_url", "url",
            "published_at", "posted_ago",
            "source", "external_id",
        ]

    def get_description_short(self, obj):
        txt = obj.description or ""
        return (txt[:180] + "…") if len(txt) > 180 else txt

    def get_posted_ago(self, obj):
        if not obj.published_at:
            return ""
        delta = timezone.now() - obj.published_at
        # simple humanize
        if delta < timedelta(minutes=1): return "just now"
        if delta < timedelta(hours=1):   return f"{delta.seconds//60}m ago"
        if delta < timedelta(days=1):    return f"{delta.seconds//3600}h ago"
        return f"{delta.days}d ago"