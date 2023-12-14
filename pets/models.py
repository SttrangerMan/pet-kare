from django.db import models


# Create your models here.


class PetSexOption(models.TextChoices):
    Male = "Male"
    Female = "Female"
    Default = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20,
        choices=PetSexOption.choices,
        default=PetSexOption.Default,
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )
    traits = models.ManyToManyField("traits.Trait")
