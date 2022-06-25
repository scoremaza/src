from logging import raiseExceptions
from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    password        = serializers.CharField(write_only=True, required=False)
    old_password    = serializers.CharField(write_only=True, required=False)
    username        = serializers.CharField(read_only=True)
    
    def validate(self, data):
        request_method = self.context['request'].method
        password       = data.get('password', None)
        if request_method == 'POST':
            if password == None:
                raise serializers.ValidationError({ 'info': 'Must use a password when creating an account. \
                                                Please enter password for your safety.'})
        elif request_method == 'PUT' or request_method == 'PATCH':
            old_password = data.get('old_password', None)
            if old_password == None and password != None:
                raise serializers.ValidationError({'info': "Please provider the correct old password"})
        
        return data
                
    
    def create(self, validate_data):
        password    = validate_data.pop('password')
        user        = User.objects.create(**validate_data)
        user.set_password(password)
        user.save()
        
        return user

    def update(self, instance, validate_data):
        
        try:
            user = instance
            password = validate_data.pop('password')
            old_password = validate_data.pop('old_password')
            if user.check_password(old_password):
                user.set_password(password)
            else:
                raise Exception('Old password doesn\'t match current password')
            user.save()
        except Exception as err:
            raise serializers.ValidationError(err)
        return super(UserSerializer,self).update(instance, validate_data)
    
    
    class Meta:
        model=User
        fields=['email','username','id','url','first_name','last_name', 'password', 'old_password']