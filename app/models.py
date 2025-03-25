from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from .managers import UserManager

#phone number validator
phone_validator = RegexValidator(
    regex=r'^\d{9}$',
    message="Enter a valid phone number with country code (e.g., 123456789).",
)

#create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=9, validators=[phone_validator])

    username = None
    email = models.EmailField(unique=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    
    def __str__(self) -> str:
        return f"User(id={self.id})"
    
class Raports(models.Model):
    class RaportTypeChoices(models.TextChoices):
        LOST = "Lost"
        FOUND = "Found"
    class AnimalTypeChoices(models.TextChoices):
        CAT = "Cat"
        DOG = "Dog"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="raports")
    raport_type = models.CharField(max_length=5, choices=RaportTypeChoices)
    animal_type = models.CharField(max_length=3, choices=AnimalTypeChoices)

    class Meta:
        verbose_name = "Raport"
        verbose_name_plural = "Raports" 

    def __str__(self) -> str:
        return f"Raport(id={self.id})"

class Images(models.Model):
    image = models.ImageField(upload_to="animal_images")
    image_attributes = models.FileField(upload_to="animal_attributes", validators=[FileExtensionValidator(["csv"])])
    raport = models.ForeignKey(Raports, on_delete=models.CASCADE, related_name="images")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images" 

    def __str__(self) -> str:
        return f"Image(id={self.id})"