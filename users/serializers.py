from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=False)
    
    def create(self, validate_data):
        password = validate_data.pop['password']
        user = User.objects.create(**validate_data)
        user.set_password(password)
        user.save()
        
        return user

    
    class Meta:
        model=User
        fields=['email','id','username','url','first_name','last_name', 'password']