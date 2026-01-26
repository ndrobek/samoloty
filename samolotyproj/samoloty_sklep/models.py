from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


def clean(self):
    if self.price <= 0:
        raise ValidationError("Price cannot be less than 1!")
    if self.stock < 0:
        raise ValidationError("Stock cannot be negative.")


def validate_capitalized(value):
    if not value:
        raise ValidationError("Field cannot be empty!")
    if not value[0].isupper():
        raise ValidationError("Entry has to start with an UPPERCASE LETTER!")



MANUFACTURERS = (
    ('BO', 'Boeing'),
    ('AI', 'Airbus'),
    ('EM', 'Embraer'),
    ('CS', 'Cessna'),
    ('OT', 'Other'),
)

MATERIALS = (
    ('PC', 'Plastic'),
    ('ML', 'Metal'),
    ('PH', 'Plush'),
    ('LR', 'Leather'),
)



# TYLKO ubrania

CLOTHING_MATERIALS = (
    ('CN', 'Cotton'),
    ('PR', 'Polyester'),
    ('AC', 'Acrylic'),
    ('WL', 'Wool'),
)

class ClothingMaterial(models.Model):
    code = models.CharField(max_length=2, choices=CLOTHING_MATERIALS, unique=True)

    def __str__(self):
        return self.get_code_display()
    


#TYLKO modele samolotów

MODEL_SCALES = (
    ('1:72', 'Scale 1:72'),
    ('1:144', 'Scale 1:144'),
    ('1:200', 'Scale 1:200'),
    ('1:400', 'Scale 1:400'),
)

AIRPLANE_MODEL_MATERIALS = (
    ('PC', 'Plastic'),
    ('ML', 'Metal'),
)

AIRPLANE_MODEL_MANUFACTURERS = (
    ('BO', 'Boeing'),
    ('AI', 'Airbus'),
    ('EM', 'Embraer'),
    ('CS', 'Cessna'),
)




class Clothing(models.Model):
    CLOTHING_TYPES = (
        ('TE', 'T-shirt'),
        ('HE', 'Hoodie'),
        ('CP', 'Cap'),
    )

    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    name = models.CharField(max_length=100, validators=[validate_capitalized])
    clothing_type = models.CharField(max_length=2, choices=CLOTHING_TYPES)
    size = models.CharField(max_length=2, choices=SIZES, blank=True, null=True)
    material = models.ManyToManyField(ClothingMaterial, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Clothing"
        verbose_name_plural = "Clothing"

    def clean(self):
        if self.clothing_type == 'CP' and self.size:
            raise ValidationError("Caps have a universal size.")        
        if self.price <= 0:
            raise ValidationError("Price cannot be less than 1!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"{self.name} ({self.size})"



class AirplaneModel(models.Model):
    name = models.CharField(max_length=100, validators=[validate_capitalized])
    aircraft_type = models.CharField(max_length=100, validators=[validate_capitalized])
    scale = models.CharField(max_length=10, choices=MODEL_SCALES)
    manufacturer = models.CharField(max_length=2, choices=AIRPLANE_MODEL_MANUFACTURERS)
    material = models.CharField(max_length=2, choices=AIRPLANE_MODEL_MATERIALS)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    def clean(self):
        if self.scale == '1:400' and self.material == 'PC':
            raise ValidationError(
                "1:400 scaled models cannot be made of plastic."
            )
        if self.price <= 0:
            raise ValidationError("Price cannot be less than 1!")        

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name} ({self.scale})"



class PlushToy(models.Model):
    name = models.CharField(max_length=100, validators=[validate_capitalized],)
    character = models.CharField(max_length=100, help_text="E.G.: plane, pilot, stewardess", validators=[validate_capitalized],)
    manufacturer = models.CharField(max_length=2, choices=MANUFACTURERS)
    material = models.CharField(max_length=2, choices=MATERIALS, default='PH', editable=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.material != 'PH':
            raise ValidationError("A plush toy has to be made of the material PLUSH.")
        if self.price <= 0:
            raise ValidationError("Price cannot be less than 1!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class LuggageTag(models.Model):
    name = models.CharField(max_length=100, validators=[validate_capitalized])
    design = models.CharField(max_length=100, help_text="E.G.: BOEING LOGO, CALL SIGN")
    manufacturer = models.CharField(max_length=2,choices=MANUFACTURERS)
    material = models.CharField(max_length=2, choices=MATERIALS)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.design != self.design.upper():
            raise ValidationError("The design has to be written in UPPERCASE LETTERS")
        if self.price <= 0:
            raise ValidationError("Price cannot be less than 1!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('PAID', 'Paid'),
        ('SHIPPED', 'Shipped'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    airplane_model = models.ForeignKey(AirplaneModel, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1) 
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NEW')

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity cannot be less than 1!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} ({self.user.username})"
