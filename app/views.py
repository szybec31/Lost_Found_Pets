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
            serializer.save()
            return Response(serializer.data)  # Zwracanie zapisanych danych
        else:
            return Response(serializer.errors)  # Zwracanie błędów walidacji

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

            # Sprawdzenie, czy użytkownik chce porównać obrazy
            compare_images = request.query_params.get('compare', 'false').lower() == 'true'
            comparison_results = []

            if compare_images:
                # Wykonaj porównanie tylko raz, dla całego zgłoszenia
                similar_images = self.compare_features(raport, raport.animal_type)
                comparison_results = similar_images  # bez opakowania w "image": ...

            response_data = serializer.data
            if comparison_results:
                response_data['comparison_results'] = comparison_results

            return Response(response_data, status=status.HTTP_200_OK)
        except Raports.DoesNotExist:
            return Response({"detail": "Raport not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

    def compare_features(self, raport, animal_type):
        target_raport_type = 'Lost' if raport.raport_type == 'Found' else 'Found'

        existing_images = Images.objects.filter(
            raport__raport_type=target_raport_type,
            raport__animal_type=animal_type
        ).select_related('raport')

        if not existing_images.exists():
            return [{"detail": "Brak obrazów w bazie do porównania."}]

        user_features_list = []
        for img in raport.images.all():
            if img.features:
                features = np.fromstring(img.features, sep=',')
                if features.size:
                    user_features_list.append(features)

        if not user_features_list:
            return [{"detail": "Brak prawidłowych wektorów cech w zgłoszeniu użytkownika."}]

        features_list = []
        image_data = []
        for img in existing_images:
            if img.features:
                features = np.fromstring(img.features, sep=',')
                if features.size:
                    features_list.append(features)
                    image_data.append({
                        "id": img.raport.id,
                        "raport_type": img.raport.raport_type,
                        "animal_type": img.raport.animal_type,
                        "date_added": img.raport.date_added.isoformat(),
                        "image": img.image.url,
                        "raport_id": img.raport.id
                    })

        if not features_list:
            return [{"detail": "Brak prawidłowych wektorów cech do porównania."}]

        dimension = 1280
        index = faiss.IndexFlatL2(dimension)
        features_array = np.array(features_list, dtype=np.float32)
        index.add(features_array)

        # Oblicz dystanse do WSZYSTKICH obrazów dla KAŻDEGO wektora użytkownika
        user_features_array = np.array(user_features_list, dtype=np.float32)
        distances_matrix, indices_matrix = index.search(user_features_array, len(features_list))

        raport_scores = {}

        # Sumuj najlepsze (najmniejsze) odległości per raport_id
        for user_idx in range(len(user_features_list)):
            for i in range(len(indices_matrix[user_idx])):
                idx = indices_matrix[user_idx][i]
                distance = distances_matrix[user_idx][i]
                img_data = image_data[idx]
                raport_id = img_data['raport_id']

                if raport_id not in raport_scores or distance < raport_scores[raport_id]['distance']:
                    raport_scores[raport_id] = {
                        "id": img_data['id'],
                        "raport_type": img_data['raport_type'],
                        "animal_type": img_data['animal_type'],
                        "date_added": img_data['date_added'],
                        "image": img_data['image'],
                        "distance": float(distance)
                    }

        # Zwróć tylko 3 najlepsze dopasowania — bez podziału na zdjęcia użytkownika
        sorted_raports = sorted(raport_scores.values(), key=lambda x: x['distance'])[:3]
        return sorted_raports
        
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
