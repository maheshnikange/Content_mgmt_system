from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer,UserSerializer,ContentItemSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .models import ContentItem
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            hashed_password = make_password(password)
            
            user = serializer.save(password=hashed_password)

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ContentItemCreateView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user  # Authenticated user from token
        data = request.data
        data['author'] = user.id  # Include the author ID in the data

        serializer = ContentItemSerializer(data=data, context={'request': request})  # Pass request context

        if serializer.is_valid():  # Validate the serializer
            try:
                serializer.save()  # Save the object
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'error': 'IntegrityError occurred while saving the content item.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'error': 'An error occurred while processing the request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ContentItemList(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            content_items = ContentItem.objects.filter(author_id=request.user.id)
            serializer = ContentItemSerializer(content_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'An error occurred while processing the request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentItemDeleteView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [TokenAuthentication]

    def delete(self, request, item_id):
        try:
            print(item_id,'-----')
            content_item = ContentItem.objects.get(id=item_id, author=request.user)
            content_item.delete()
            return Response({'message': 'Content item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except ContentItem.DoesNotExist:
            return Response({'error': 'Content item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred while processing the request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminContentItemList(APIView):
    permission_classes = (AllowAny, IsAdminUser)
    authentication_classes = [TokenAuthentication]


    def get(self, request):
        content_items = ContentItem.objects.all()
        serializer = ContentItemSerializer(content_items, many=True)
        return Response(serializer.data)
