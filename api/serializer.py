from rest_framework import serializers
from .models import Project, Users, Member, Step ,Resource, ResourceAllocation
from django.contrib.auth.hashers import make_password

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','name', 'description', 'date','status')

class Member_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class Step_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id','name','email','password')
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        print("Hello11")
        user = Users.objects.create(
            name = validated_data['name'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)