from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Tarea")
    completada = models.BooleanField(default=False, verbose_name="¿Completada?")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return self.nombre

# Create your models here.

class programmer(models.Model):
    fullname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
