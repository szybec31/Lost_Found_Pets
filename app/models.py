from datetime import date
from django.utils.timezone import now

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator, FileExtensionValidator
from .managers import UserManager

#phone number validator
phone_validator = RegexValidator(
    regex=r'^\d{9}$',
    message="Enter a valid phone number with country code (e.g., 123456789).",
)
# model Admina
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):  # Tworzenie nowego użytkownika
        if not email:  # Sprawdzanie, czy podano email
            raise ValueError('The Username field must be set')

        # Ustawienie domyślnych wartości dla opcjonalnych pól
        extra_fields.setdefault('phone', 'Unknown')
        extra_fields.setdefault('first_name', 'No Name')
        extra_fields.setdefault('last_name', 'No Name')
        #extra_fields.setdefault('is_superuser', 0)
        extra_fields.setdefault('last_login', date.today())
        extra_fields.setdefault('date_joined', date.today())

        user = self.model(email=email, **extra_fields)  # Tworzenie instancji modelu użytkownika
        user.set_password(password)  # Haszowanie hasła
        user.save(using=self._db)  # Zapis użytkownika w bazie danych
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        # Ustawienie wymaganych pól dla superużytkownika
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# model Usera
class UserModel(AbstractBaseUser, PermissionsMixin):

    id = models.BigAutoField(primary_key=True, db_column='id')
    email = models.EmailField(unique=True,db_column='email')
    phone = models.CharField(max_length=9, validators=[phone_validator],db_column='phone_number')
    first_name = models.CharField(max_length=30,db_column='first_name')
    is_superuser = models.IntegerField(default=0,db_column='is_superuser')
    is_staff = models.IntegerField(default=0,db_column='is_staff')
    is_active = models.IntegerField(default=0,db_column='is_active')
    last_name = models.CharField(max_length=30,db_column='last_name')
    last_login = models.DateTimeField(db_column='last_login')
    date_joined = models.DateTimeField(default=now,db_column='date_joined')

    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "app_user"

    def __str__(self):
        return self.email#f"User(id={self.id})"
    
class Raports(models.Model):
    class RaportTypeChoices(models.TextChoices):
        LOST = "Lost"
        FOUND = "Found"
    class AnimalTypeChoices(models.TextChoices):
        CAT = "Cat"
        DOG = "Dog"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="raports")
    raport_type = models.CharField(max_length=5, choices=RaportTypeChoices)
    animal_type = models.CharField(max_length=3, choices=AnimalTypeChoices)
    date_added = models.DateTimeField(default=now)
    description = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Raport"
        verbose_name_plural = "Raports" 

    def __str__(self) -> str:
        return f"Raport(id={self.id})"

class RaportsLink(models.Model):
    raport_link1 = models.ForeignKey(Raports, on_delete=models.CASCADE, related_name="raport_link1")
    raport_link2 = models.ForeignKey(Raports, on_delete=models.CASCADE, related_name="raport_link2")

    class Meta:
        verbose_name = "Raport_Linked"
        verbose_name_plural = "Raports_Linked" 

    def __str__(self) -> str:
        return f"RaportLink(id={self.id})"
    
class Images(models.Model):
    image = models.ImageField(upload_to="animal_images")
    image_attributes = models.FileField(upload_to="animal_attributes", validators=[FileExtensionValidator(["csv"])])
    raport = models.ForeignKey(Raports, on_delete=models.CASCADE, related_name="images")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images" 

    def __str__(self) -> str:
        return f"Image(id={self.id})"