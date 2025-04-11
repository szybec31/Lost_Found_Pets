from rest_framework import serializers
from .models import UserModel, Raports, Images


# Serializer od użytkownika
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel  # Powiązanie z modelem od klienta
        fields = ['email', 'password', 'phone','first_name','last_name']  # Pola do serializacji z bazy danych
        extra_kwargs = {"password": {"write_only": True}}  # Hasło dostępne tylko do zapisu niewidoczne w odpowiedzi

    # Tworzenie użytkownika
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            phone = validated_data['phone'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        return user

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
        fields = ['id','user_id','raport_type','animal_type','date_added','address','description','images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        raport = Raports.objects.create(**validated_data)

        for image in uploaded_images:
            Images.objects.create(raport=raport, image=image)

        return raport

