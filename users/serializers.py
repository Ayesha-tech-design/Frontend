from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'profile_picture', 'bio']
        # Hum nahi chahte ke koi student apna username ya role (e.g. Student se Teacher) khud change kare
        read_only_fields = ['username', 'role']