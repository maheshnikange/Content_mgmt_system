from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .models import ContentItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'country', 'pincode')

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = '__all__'

    def validate_title(self, value):
        if len(value) > 30:
            raise serializers.ValidationError("Title cannot exceed 30 characters.")
        return value
    def validate_body(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("Body cannot exceed 300 characters.")
        return value
    def validate_summary(self, value):
        if len(value) > 60:
            raise serializers.ValidationError("Summary cannot exceed 60 characters.")
        return value