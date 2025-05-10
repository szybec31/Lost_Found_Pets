from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserModel, Raports, Images
from .ai import extract_features
from datetime import date, datetime

# Serializer od użytkownika
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel  # Powiązanie z modelem od klienta
        fields = ['email', 'password', 'phone', 'first_name', 'last_name']  # Pola do serializacji z bazy danych
        extra_kwargs = {"password": {"write_only": True}}  # Hasło dostępne tylko do zapisu niewidoczne w odpowiedzi

    # Tworzenie użytkownika
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'phone', 'first_name', 'last_name']

class Add_Raport_IMG_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id','image','raport_id']

class Add_Raport_Serializer(serializers.ModelSerializer):
    images = Add_Raport_IMG_Serializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Raports
        fields = ['id','user_id','raport_type','animal_type','date_added','district','description','images', 'uploaded_images']

    def validate_uploaded_images(self, value):
        if len(value) > 3:
            raise serializers.ValidationError("Można dodać maksymalnie 3 zdjęcia.")
        return value

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        raport = Raports.objects.create(**validated_data)

        for image in uploaded_images:
            # Images.objects.create(raport=raport, image=image)
            temp_instance = Images(raport=raport, image=image)
            temp_instance.save()

            image_path = temp_instance.image.path
            features = extract_features(image_path)
            features_str = ",".join(map(str, features))

            temp_instance.features = features_str
            temp_instance.save()

        return raport

class RaportWithImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Raports
        fields = ['id', 'raport_type', 'animal_type', 'date_added', 'image']

    def get_image(self, obj):
        image = obj.images.first()  # tylko jedno zdjęcie
        return image.image.url if image else None
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image']

class RaportDetailSerializer(serializers.ModelSerializer):  # wszystkie zdjęcia
    images = ImageSerializer(many=True, read_only=True)
    user = UserPublicSerializer(source='user_id')

    class Meta:
        model = Raports
        fields = ['id', 'raport_type', 'animal_type', 'description', 'date_added', 'user', 'images']

class RaportWithMultipleImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Raports
        fields = ['id', 'raport_type', 'animal_type', 'date_added', 'image']

    def get_image(self, obj):
        image = obj.images.first()  #kilka zdjęć
        return [image.image.url for image in obj.images.all()[:3]]
