from django.shortcuts import render
from rest_framework.views import APIView
from my_app.serializers import UserPasswordResetSerializer, UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, SendPasswordResetEmailSerializer
from django.contrib.auth import authenticate
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from my_app.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration Successful'},
            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username', 'email')
            password = serializer.data.get('password')
            user = authenticate(username=username, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Username or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception =True):
            return Response({'msg':'Password Reset Link send. Please check your Email'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status. HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format = None):
        serializer = UserPasswordResetSerializer(data = request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    