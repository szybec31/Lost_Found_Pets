from datetime import date, datetime

from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import UserModel, Raports
from .serializers import UserSerializer, Add_Raport_Serializer, RaportWithImageSerializer
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
        print(request.data)
        response = super().post(request, *args, **kwargs)
        print(response)
        print(request)
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
    permission_classes = [AllowAny]

    def get(self, request):
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)  # Zwraca listę użytkowników

    def post(self,request):
        print(request.data)
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

class User_info(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):  # Żądanie GET
        print(request.user)
        email = request.user
        user = get_user_model()
        user_info = user.objects.get(email=email)  # Pobieranie wszystkich danych o uzytkowniku
        serializer = UserSerializer(user_info)  # Serializacja listy danych usera (przekształcanie obiektów w listę słowników)
        return Response(serializer.data)  # Dane zwracane w formacie Json

    def post(self,request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been changed."}, status=status.HTTP_200_OK)


class RaportsWithOneImageView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RaportWithImageSerializer

    def get_queryset(self):
        return Raports.objects.annotate(image_count=Count('images')).filter(image_count__gte=1).prefetch_related('images').order_by('-date_added')