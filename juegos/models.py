from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    descripcion = models.TextField()
    url_imagen = models.CharField(max_length=100, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categorias', default=1)

    def __str__(self):
        return self.nombre
    

