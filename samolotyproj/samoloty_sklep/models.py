from django.db import models
from django.core.exceptions import ValidationError


MODEL_SCALES = (
    ('1:72', 'Skala 1:72'),
    ('1:144', 'Skala 1:144'),
    ('1:200', 'Skala 1:200'),
    ('1:400', 'Skala 1:400'),
)

MATERIALS = (
    ('PC', 'Plastik'),
    ('ML', 'Metal'),
    ('PH', 'Plusz'),
    ('LR', 'Skóra'),
)

MANUFACTURERS = (
    ('BO', 'Boeing'),
    ('AI', 'Airbus'),
    ('EM', 'Embraer'),
    ('CS', 'Cessna'),
    ('OT', 'Other'),
)



# Kubki itp.

class Cup(models.Model):
    CUP_TYPES = (
        ('KK', 'Kubek'),
        ('TS', 'Termos'),
        ('BA', 'Butelka'),
    )

    capacity_ml = models.PositiveIntegerField()
    material = models.CharField(max_length=2, choices=MATERIALS)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.capacity_ml < 100:
            raise ValidationError("Pojemność kubka musi być równa lub większa niż 100 ml.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.capacity_ml} ml"

# Ubrania

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

    name = models.CharField(max_length=100)
    clothing_type = models.CharField(max_length=2, choices=CLOTHING_TYPES)
    size = models.CharField(max_length=2, choices=SIZES)
    material = models.CharField(max_length=2, choices=MATERIALS)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.size})"




# Model samolotu

class AirplaneModel(models.Model):
    name = models.CharField(max_length=100)
    aircraft_type = models.CharField(max_length=100)
    scale = models.CharField(max_length=10, choices=MODEL_SCALES)
    manufacturer = models.CharField(max_length=2, choices=MANUFACTURERS)
    material = models.CharField(max_length=2, choices=MATERIALS)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    def clean(self):
        if self.scale == '1:400' and self.material == 'PC':
            raise ValidationError(
                "Modele w skali 1:400 nie mogą być wykonane z plastiku."
            )
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name} ({self.scale})"


# Pluszowe samoloty :)
class PlushToy(models.Model):
    name = models.CharField(max_length=100)
    character = models.CharField(max_length=100, help_text="Przykładowo: samolot, pilot, stewardessa")
    manufacturer = models.CharField(max_length=2, choices=MANUFACTURERS)
    material = models.CharField(max_length=2, choices=MATERIALS, default='TX')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# Zawieszki na walizkę

class LuggageTag(models.Model):
    name = models.CharField(max_length=100)
    design = models.CharField(max_length=100, help_text="Przykładowo: BOEING LOGO, CALL SIGN")
    manufacturer = models.CharField(max_length=2,choices=MANUFACTURERS)
    material = models.CharField(max_length=2, choices=MATERIALS)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name




# Inne (miscellaneous akcesoria)

class OtherGadget(models.Model):
    name = models.CharField(max_length=100)
    accessory_type = models.CharField(max_length=100, help_text="Przykładowo: plecak, torba, portfel")
    manufacturer = models.CharField(max_length=2, choices=MANUFACTURERS)
    material = models.CharField(max_length=2, choices=MATERIALS)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
