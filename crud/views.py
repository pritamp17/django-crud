from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import bcrypt

from .models import UserModel
from .serializers import UserProfileSerializer

class WelcomeView(APIView):
     def get(self, request):
          return Response({'Hii': 'SignUp or Login'})
     
class SignUpView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        bio = request.data.get('bio', '')
        profile_picture = request.data.get('profile_picture')

        if UserModel.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not name or not email or not password:
            return Response({'error': 'Please provide name, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = UserModel(name=name, email=email, password=hashed_password, bio=bio, profile_picture=profile_picture)
        user.save()
        return Response({'message': 'Cool! Sign up successful, Now you can login'})

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(request)
        if not email or not password:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'error': 'User with the specified email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        authenticated_User = None

        if email is not None and password is not None: 
            stored_password = user.password.encode('utf8')
            is_check = bcrypt.checkpw(password.encode('utf8'), stored_password)
            if is_check:
                authenticated_User = user
            else:
                authenticated_User = None
       
        print(authenticated_User)
        if authenticated_User is not None:
            refresh = RefreshToken.for_user(authenticated_User)
            access_token = str(refresh.access_token)
            return Response({'Welcome': authenticated_User.name, 'access_token': access_token})
        
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Logout successful'})
    
class UpdateProfileView(APIView):
     permission_classes = [IsAuthenticated]

     def patch(self, request):
        # print(request.META)
        email = request.data.get('email') 
        try:
            profile = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        updated_data = {}

        if 'name' in request.data:
            updated_data['name'] = request.data['name']

        if 'password' in request.data:
            updated_data['password'] = request.data['password']

        if 'bio' in request.data:
            updated_data['bio'] = request.data['bio']

        if 'profile_picture' in request.data:
            updated_data['profile_picture'] = request.data['profile_picture']

        serializer = UserProfileSerializer(profile, data=updated_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def delete(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            toBeDeletedEmail=request.get('email')
            user_id = JWTAuthentication().get_user(token).id
            user = UserModel.objects.get(id=user_id)
            userToBeDeleted = UserModel.objects.get(email=toBeDeletedEmail)
            if user.email != "admin@gmail.com":
                return Response({'error': 'Only the admin user can perform this action'}, status=status.HTTP_403_FORBIDDEN)

            userToBeDeleted.delete()
            return Response({'message': 'User profile deleted successfully'})
        except Exception as e:
            return Response({'error': 'An error occurred while deleting the user profile'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    