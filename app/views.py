from datetime import date, datetime

from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import UserModel, Raports, Images
from .serializers import UserSerializer, Add_Raport_Serializer, RaportWithImageSerializer, RaportDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .ai import *
import faiss



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

    def post(self, request):
        data = request.data
        data['date_added'] = datetime.now()
        data['user_id'] = request.user.id if request.user.is_authenticated else None  # Ustawianie ID użytkownika

        serializer = Add_Raport_Serializer(data=data)

        if serializer.is_valid():
            report = serializer.save()  # Zapisywanie raportu w bazie

            # Każdy dodany obraz do bazy jest od razu porównywany za pomocą jego wektora cech
            for image in report.images.all():
                self.compare_features(image)

            return Response(serializer.data)  # Zwracanie zapisanych danych
        else:
            return Response(serializer.errors)  # Zwracanie błędów walidacji

    def compare_features(self, new_image):
        # Pobieranie wszystkich wektorów cech z bazy danych oprócz tego z nowego zdjęcia
        existing_images = Images.objects.exclude(id=new_image.id)

        if not existing_images.exists():  # Przypadek, kiedy baza jest pusta
            print("Brak obrazów w bazie do porównania.")
            return

        features_list = []  # Lista do przechowywania wektorów cech
        image_paths = []   # Lista do przechowywania ścieżek obrazów

        for img in existing_images:
            # Wczytywanie wektora cech przechowywanego oryginalnie jako tekst do tablicy numpy
            features = np.fromstring(img.features, sep=',')
            features_list.append(features)
            image_paths.append(img.image.url)

        # Inicjalizacja FAISS dla porównywania wektorów cech
        dimension = 1280  # Długość wektora cech MobileNetV2
        index = faiss.IndexFlatL2(dimension)

        # Dodanie wektorów cech z bazy do indeksu FAISS
        features_array = np.array(features_list, dtype=np.float32)
        index.add(features_array)

        # Przygotowanie wektora cech nowego obrazu
        new_features = np.fromstring(new_image.features, sep=',').reshape(1, -1)
        distances, indices = index.search(new_features, 3) # Wyszukiwanie trzech najbardziej podobnych obrazów
        # (im mniejsza odległość, tym bardziej podobne)

        similar_images = []  # Lista do przechowywania wyników podobnych obrazów

        for idx in range(len(indices[0])):
            image_path = image_paths[indices[0][idx]]  # Pobieranie ścieżki obrazu
            distance = distances[0][idx]  # Pobieranie odległości
            similar_images.append((image_path, distance))

        if similar_images:  # Jeśli znaleziono podobne obrazy
            print("Podobne obrazy dla nowo-dodanego obrazu o ID: ", new_image.id)
            for img_path, distance in similar_images:
                print(f"Obraz: {img_path}, Odległość: {distance:.4f}")
        else:
            print("Brak podobnych obrazów dla nowo-dodanego obrazu o ID: ", new_image.id)

class Raport_Details(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            raport = Raports.objects.get(pk=pk)
            serializer = RaportDetailSerializer(raport)
            return Response(serializer.data)
        except Raports.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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

class RaportsFiltered(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RaportWithImageSerializer

    def get_queryset(self):
        queryset = Raports.objects.annotate(image_count=Count('images')).filter(image_count__gte=1).prefetch_related('images').order_by('-date_added')
        raport_type = self.request.query_params.get('raport_type')  #Lost/Found
        animal_type = self.request.query_params.get('animal_type')  #Cat/Dog

        if raport_type:
            queryset = queryset.filter(raport_type=raport_type)
        if animal_type:
            queryset = queryset.filter(animal_type=animal_type)
        return queryset
    
class UserRaportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        raports = Raports.objects.filter(user_id=user.id)
        serializer = RaportDetailSerializer(raports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserRaportDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            raport = Raports.objects.get(pk=pk, user_id=request.user.id)
            serializer = RaportDetailSerializer(raport)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Raports.DoesNotExist:
            return Response({"detail": "Raport not found or access denied."}, status=status.HTTP_404_NOT_FOUND)
        
class UpdateUserRaportView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            raport = Raports.objects.get(pk=pk, user_id=request.user.id)
        except Raports.DoesNotExist:
            return Response({"detail": "Raport not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        serializer = Add_Raport_Serializer(raport, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
