from rest_framework import serializers
from .models import User, referal_req, Referer, Referral_post, Job, SeekerRequest
from rest_framework import serializers
from .models import User, SeekerRequest
from django.utils import timezone
from datetime import timedelta
from django.utils.timesince import timesince
from .models import Profile, Experience, Project, Education, Random1



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
        



class SeekerRequestMiniSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source="requester.username", read_only=True)
    class Meta:
        model = SeekerRequest
        fields = ["id", "requester_name", "message", "status"]


## Creating another serializer for posting REFERRAL in DB 
class ReferralPostSerializer(serializers.ModelSerializer):
    seeker_requests = serializers.SerializerMethodField()
    referrer_name = serializers.CharField(source="user.username", read_only=True)
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Referral_post
        fields = [
            "id",
            "company_name",
            "role",
            "referral_domains",
            "job_description",
            "experience_required",
            "availability",
            "location",
            "salary_expectation",
            "link_to_apply",
            "created_at",
            "referrer_name",
            "time_since",
            "seeker_requests",
        ]

    def get_seeker_requests(self, obj):
        context = self.context
        requests = obj.seeker_requests.all()
        return SeekerRequestSerializer(requests, many=True, context=context).data

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
    

#serialiser for seeker request
class SeekerRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source="requester.username", read_only=True)
    resume = serializers.FileField(required=False)
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = SeekerRequest
        fields = "__all__"
        read_only_fields = ["requester", "referrer", "status", "created_at", "updated_at"]

    def get_resume_url(self, obj):
        request = self.context.get("request")
        if obj.resume:
            if request:
                return request.build_absolute_uri(obj.resume.url)
            return obj.resume.url
        return None




#Serialiaser for User Profile 


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'role_name', 'company', 'duration', 'description']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'link', 'brief']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school', 'field_of_study', 'achievements']


class ProfileSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'name', 'title', 'quote', 'about',
            'profile_pic', 'linkedin', 'github', 'other_link',
            'skills', 'experiences', 'projects', 'educations', 'updated_at'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        experiences_data = validated_data.pop('experiences', [])
        projects_data = validated_data.pop('projects', [])
        educations_data = validated_data.pop('educations', [])

        profile = Profile.objects.create(**validated_data)

        for exp in experiences_data:
            Experience.objects.create(profile=profile, **exp)
        for proj in projects_data:
            Project.objects.create(profile=profile, **proj)
        for edu in educations_data:
            Education.objects.create(profile=profile, **edu)

        return profile

    def update(self, instance, validated_data):
        experiences_data = validated_data.pop('experiences', [])
        projects_data = validated_data.pop('projects', [])
        educations_data = validated_data.pop('educations', [])

        # Update base profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Replace experiences / projects / educations
        instance.experiences.all().delete()
        instance.projects.all().delete()
        instance.educations.all().delete()

        for exp in experiences_data:
            Experience.objects.create(profile=instance, **exp)
        for proj in projects_data:
            Project.objects.create(profile=instance, **proj)
        for edu in educations_data:
            Education.objects.create(profile=instance, **edu)

        return instance



class RandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Random1
        fields = ["name"]