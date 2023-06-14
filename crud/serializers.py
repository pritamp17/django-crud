from rest_framework import serializers
from .models import UserModel

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'