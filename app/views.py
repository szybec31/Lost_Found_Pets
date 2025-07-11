from django.utils.timezone import now
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, user_logged_in
from .models import UserModel, Raports, Images, RaportsLink
from .serializers import UserSerializer, Add_Raport_Serializer, RaportWithImageSerializer, RaportDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .ai import *
import faiss
from django.core.cache import cache
from .mail import verify_code_mail, custom_mail
from .Generator import generate_verify_code
import threading
import time
import os
from django.conf import settings


# Create your views here.

# Widok do listowania i tworzenia użytkowników
class UserView(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()  # Zapytanie do SQL o wszystkich użytkowników
    serializer_class = UserSerializer  # Serializer do danych użytkownika
    permission_classes = [AllowAny]  # Otwarty dostęp dla wszystkich użytkowników

# Widok do uzyskiwania tokenu użytkownika
class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):  # Żądanie POST nadpisywane z TokenObtainPairView, stąd args i kwargs
        email = request.data.get("email")
        password = request.data.get("password")

        user = get_user_model().objects.filter(email=email).first()
        if user and user.check_password(password):
            # Wygeneruj kod weryfikacyjny
            code = "11" #generate_verify_code() # Tymczasowo wyłączony  !!!!

            # Przechowuj kod (np. cache z 5-minutowym TTL)
            cache.set(f"2fa_code_user_{code}", email, timeout=300)

            # Wyślij kod na email
            #verify_code_mail(email,code)               # Tymczasowo wyłączony  !!!!
            print(code)
            print("-----------")
            return Response({"detail": "Kod weryfikacyjny wysłany na email.", "success": True}, status=status.HTTP_200_OK)

        return Response({"detail": "Nieprawidłowy email lub hasło.", "success": False}, status=status.HTTP_401_UNAUTHORIZED)

class Confirm2FACodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        code = request.data.get("code")
        email = cache.get(f"2fa_code_user_{code}")
        print(code, email)

        if not email:
            return Response({"detail": "Kod nieprawidłowy lub wygasł."}, status=400)

        user = get_user_model().objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        user.last_login = now()
        user.save()  # Zapisywanie zmian w bazie danych
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })



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
        data = request.data.copy()  # Zrób kopię, żeby nie modyfikować request.data bezpośrednio
        data['date_added'] = now()

        serializer = Add_Raport_Serializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("❌ Błędy walidacji:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Raport_Details(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            raport = Raports.objects.get(pk=pk)
            serializer = RaportDetailSerializer(raport)
            return Response(serializer.data)
        except Raports.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SendRaportEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        raport = Raports.objects.get(pk=pk)
        user = raport.user
        reciver = user.email
        print(reciver)

        if not reciver:
            return Response({"error": "Użytkownik nie ma przypisanego adresu e-mail."}, status=400)
        # Dane z frontendu
        sender_email = request.user.email
        sender_name = request.user.first_name
        sender_name += f" {request.user.last_name}"
        print(sender_email, sender_name)
        message = request.data.get("message")

        if not sender_email or not sender_name or not message:
            return Response({"error": "Brakuje wymaganych danych."}, status=400)

        if sender_email.lower() == reciver.lower():
            return Response({"error": "Nie można wysłać wiadomości do samego siebie."}, status=400)

        custom_mail(sender_email,sender_name,reciver, message,pk)
        return Response({"detail": "Email został wysłany"}, status=status.HTTP_200_OK)

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
            raport = Raports.objects.get(pk=pk)
            serializer = RaportDetailSerializer(raport, context={'request': request})

            compare_images = request.query_params.get('compare', 'false').lower() == 'true'
            comparison_results = []

            if compare_images:
                similar_images = self.compare_features(raport, raport.animal_type, raport.user_id)
                comparison_results = similar_images

            response_data = serializer.data
            if comparison_results:
                response_data['comparison_results'] = comparison_results

            return Response(response_data, status=status.HTTP_200_OK)
        except Raports.DoesNotExist:
            return Response({"detail": "Raport not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

    def compare_features(self, raport, animal_type, user_id):
        target_raport_type = 'Lost' if raport.raport_type == 'Found' else 'Found'

        existing_images = Images.objects.filter(
            raport__raport_type=target_raport_type,
            raport__animal_type=animal_type
        ).exclude(raport__user_id=user_id).select_related('raport')

        if not existing_images.exists():
            return [{"detail": "Brak obrazów w bazie do porównania."}]

        # Konwersja wektorów cech z bieżącego zgłoszenia
        user_features_list = []
        for img in raport.images.all():
            if img.features:
                features = np.fromstring(img.features, sep=',')
                if features.size:
                    user_features_list.append(features)

        if not user_features_list:
            return [{"detail": "Brak prawidłowych wektorów cech w zgłoszeniu użytkownika."}]

        # Konwersja wektorów cech z istniejącej bazy
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

        # Przygotowanie danych
        dimension = 1280

        def normalize(vectors):
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            return vectors / norms

        features_array = normalize(np.array(features_list, dtype=np.float32))
        user_features_array = normalize(np.array(user_features_list, dtype=np.float32))

        # Cosine similarity via FAISS using inner product
        index = faiss.IndexFlatIP(dimension)
        index.add(features_array)

        # Szukanie podobnych obrazów
        distances_matrix, indices_matrix = index.search(user_features_array, len(features_list))

        raport_scores = {}

        for user_idx in range(len(user_features_array)):
            for i in range(len(indices_matrix[user_idx])):
                idx = indices_matrix[user_idx][i]
                similarity = float(distances_matrix[user_idx][i])  # wartość w zakresie [0,1]
                similarity_percentage = round(similarity * 100, 2)

                img_data = image_data[idx]
                raport_id = img_data['raport_id']

                if raport_id not in raport_scores or similarity > raport_scores[raport_id]['similarity']:
                    raport_scores[raport_id] = {
                        "id": img_data['id'],
                        "raport_type": img_data['raport_type'],
                        "animal_type": img_data['animal_type'],
                        "date_added": img_data['date_added'],
                        "image": img_data['image'],
                        "similarity": similarity_percentage
                    }

        # Posortuj po najwyższym podobieństwie i zwróć top 3
        sorted_raports = sorted(raport_scores.values(), key=lambda x: x['similarity'], reverse=True)[:3]
        return sorted_raports


class UpdateUserRaportView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            raport = Raports.objects.get(pk=pk, user_id=request.user.id)
        except Raports.DoesNotExist:
            return Response({"detail": "Raport not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        # Obsługa zdjęć
        images = request.FILES.getlist('images')
        if images:
            # Usuń stare zdjęcia z bazy i dysku
            old_images = Images.objects.filter(raport=raport)
            for img in old_images:
                if img.image and os.path.isfile(img.image.path):
                    try:
                        os.remove(img.image.path)
                    except Exception as e:
                        print(f"Error deleting file {img.image.path}: {e}")
            old_images.delete()
            # Dodaj nowe zdjęcia
            for img in images[:3]:  # max 3 zdjęcia
                Images.objects.create(raport=raport, image=img)

        serializer = Add_Raport_Serializer(raport, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LinkRaportsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        raport_id_1 = request.data.get('raport_id_1')
        raport_id_2 = request.data.get('raport_id_2')
#checks
        if not raport_id_1 or not raport_id_2:
            return Response({"error": "Both raport_id_1 and raport_id_2 are required."}, status=status.HTTP_400_BAD_REQUEST)

        if raport_id_1 == raport_id_2:
            return Response({"error": "Cannot link a raport to itself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            raport_1 = Raports.objects.get(pk=raport_id_1)
            raport_2 = Raports.objects.get(pk=raport_id_2)
        except Raports.DoesNotExist:
            return Response({"error": "One or both of the specified raports do not exist."}, status=status.HTTP_404_NOT_FOUND)

        if raport_1.user != request.user:
            return Response({"error": "You are not the creator of the raport."}, status=status.HTTP_403_FORBIDDEN)
        
        if RaportsLink.objects.filter(raport_link1=raport_1, raport_link2=raport_2).exists():
            return Response({"error": "This link already exists."}, status=status.HTTP_400_BAD_REQUEST)

#Linking
        RaportsLink.objects.create(raport_link1=raport_1, raport_link2=raport_2)
        if RaportsLink.objects.filter(raport_link1=raport_2, raport_link2=raport_1).exists():
            threading.Thread(target=self.delete_records, args=(raport_1.id, raport_2.id)).start()
            return Response({"message": "Raports linked and deletion scheduled."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Raports linked. Waiting for reverse link to schedule deletion."}, status=status.HTTP_201_CREATED)

#Deletion
    def delete_records(self, raport_1_id, raport_2_id):
        time.sleep(5)
        images = Images.objects.filter(raport_id__in=[raport_1_id, raport_2_id])
        for img in images:
            print(f"Próba usunięcia: {img.image.path}")
            if img.image and os.path.isfile(img.image.path):
                try:
                    os.remove(img.image.path)
                    print(f"Usunięto: {img.image.path}")
                except Exception as e:
                    print(f"Error deleting file {img.image.path}: {e}")
            else:
                print(f"Plik nie istnieje: {img.image.path}")

        images.delete()
        Raports.objects.filter(id__in=[raport_1_id, raport_2_id]).delete()
        RaportsLink.objects.filter(raport_link1=raport_1_id, raport_link2=raport_2_id).delete()
        RaportsLink.objects.filter(raport_link2=raport_1_id, raport_link1=raport_2_id).delete()
        print(f"Records for RaportsLink with raports id: {raport_1_id} and {raport_2_id} associated data have been deleted.")

