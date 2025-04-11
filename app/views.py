from datetime import date, datetime

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils.representation import serializer_repr
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import UserModel
from .serializers import UserSerializer, Add_Raport_Serializer, Add_Raport_IMG_Serializer
from rest_framework.permissions import AllowAny, IsAuthenticated



# Create your views here.

# Widok do listowania i tworzenia użytkowników
class UserView(generics.ListCreateAPIView):
    queryset = UserModel.objects.raw('SELECT * FROM app_user')  # Zapytanie do SQL o wszystkich użytkowników
    serializer_class = UserSerializer  # Serializer do danych użytkownika
    permission_classes = [AllowAny]  # Otwarty dostęp dla wszystkich użytkowników

# Widok do uzyskiwania tokenu użytkownika
class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):  # Żądanie POST nadpisywane z TokenObtainPairView, stąd args i kwargs
        response = super().post(request, *args, **kwargs)
        email = request.data['email']  # Pobieranie loginu użytkownika z danych żadania
        print("Request data:", request.data['email'])
        print(email)
        if email:
            # Pobierz model użytkownika na podstawie nazwy użytkownika
            User = get_user_model()
            try:
                user = User.objects.get(email=email)  # Szukanie użytkownika na podstawie jego loginu
                # Aktualizuj last_login
                user.last_login = date.today()
                user.save()  # Zapisywanie zmian w bazie danych
            except User.DoesNotExist:
                pass

        return response


class RegisterUser(APIView):
    def get(self, request):
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)  # Zwraca listę użytkowników

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Add_Raport(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data
        data['date_added'] = datetime.now()
        print(request.user.id)
        data['user_id'] = request.user.id
        print(data)
        serializer = Add_Raport_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Zapis raportu w bazie danych
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class Add_Raport_IMG(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data

        serializer = Add_Raport_IMG_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Zapis raportu w bazie danych
            return Response(serializer.data)
        else:
            return Response(serializer.errors)