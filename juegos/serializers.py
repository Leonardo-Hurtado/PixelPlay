from rest_framework import serializers
from .models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre'] #campos a incluir en la Api