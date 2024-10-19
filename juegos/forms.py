from django import forms
from .models import Categoria
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'genero', 'descripcion', 'precio']

