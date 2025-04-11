from rest_framework import serializers
from .models import UserModel, Raports


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

class Add_Raport_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Raports
        fields = ['id','user_id','raport_type','animal_type','date_added','address','description']
