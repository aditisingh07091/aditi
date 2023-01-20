
from xml.dom import ValidationErr
from rest_framework import serializers
from my_app.models import User
from django.utils.encoding import smart_str, force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}
    , write_only=True)
    class Meta:
        model = User
        fields = ['email','username','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        username=attrs.get("username")
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        """if len(username) < 5 :
            raise serializers.ValidationError("Username must have 6 character")
        if len(username) > 12:
            raise serializers.ValidationError("Username should have less then 12 characters")
        if len(password) < 7:
            raise serializers.ValidationError("Enter 8 digit Password")
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does not match")
        return attrs"""
    
        SpecialSym =['$', '@', '#', '%']

        if len(username) < 5 :
            raise serializers.ValidationError("Username must have 6 character")
        
        if len(username) > 20:
            raise serializers.ValidationError('Password length should be not be greater than 8')
        
        if len(password) < 6:
            raise serializers.ValidationError('Password length should be at least 6')
         
        if len(password) > 20:
            raise serializers.ValidationError('Password length should be not be greater than 8')

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password should have at least one numeral')
         
        if not any(char in SpecialSym for char in password):
            raise serializers.ValidationError('Password should have at least one of the symbols $@#')
        
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError('Password should have at least one uppercase letter')
         
        if not any(char.islower() for char in password):
            raise serializers.ValidationError('Password should have at least one lowercase letter')
            
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does not match")
        
        return attrs
        

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username', 'password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['id','email','username']
        
class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email = email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        print('Encoded UID', uid)
        token = PasswordResetTokenGenerator().make_token(user)
        print('Password Reset Token', token)
        link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
        print('Password Reset Link', link)
        # Send EMail
        body = 'Click Following Link to Reset Your Password '+link
        data = {
            'subject':'Reset Your Password',
            'body':body,
            'to_email':user.email
        }
        return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

    
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, style={'imput_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=50, style={'imput_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
    
    def validate(self, attrs):
        try:
            password = attrs.get('passwrod')
            password2 = attrs.get('passwrod2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(" Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token in not Valid or Expired')
    
    