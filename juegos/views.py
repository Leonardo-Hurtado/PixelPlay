from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .models import Producto, Categoria
from .forms import ProductoForm
from django.http import HttpResponse
from .serializers import CategoriaSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
import requests
from django.core.cache import cache
from django.urls import reverse_lazy
import random



class CustomLoginView(LoginView):
    template_name = 'juegos/login.html'

def detalle_juego(request, pk):
    juego = cache.get("detalle_juego")
    url = f"https://www.freetogame.com/api/game?id={pk}"
    response = requests.get(url) #realizar solicitud Get a la Api
    juego = response.json()  #convertir la respuesta a formato Json
    numero_aleatorio = random.randint(10000, 59990)
    juego['precio'] = "{:,}".format(numero_aleatorio).replace(",", ".")
    cache.set("detalle_juego", juego, timeout = 60*60)
    return render(request, 'juegos/detalle_juego.html', {'juego': juego})

def detalle_categoria(request, pk):
    categoria=get_object_or_404(Categoria, pk=pk)
    url = f"https://www.freetogame.com/api/games?category={categoria.nombre}"
    response = requests.get(url) #realizar solicitud Get a la Api
    juegos = response.json()  #convertir la respuesta a formato Json
    for juego in juegos:
        numero_aleatorio = random.randint(10000, 59990)
        juego['precio'] = "{:,}".format(numero_aleatorio).replace(",", ".")
        
    #paginator = Paginator(juego, 6)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    
    return render(request, 'juegos/detalle_categoria.html', {'categoria': categoria, 'juegos': juegos})


# ViewSet para el modelo Producto
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()  # Recuperar todos los productos de la base de datos
    serializer_class = CategoriaSerializer  # Usar el serializador definido para Producto
    permission_classes = [IsAuthenticated]  # Requiere que el usuario esté autenticado para acceder



@login_required
def home(request):
    context = {
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'juegos/home.html', context)


def index(request):
    query = request.GET.get('q')
    url = "https://www.freetogame.com/api/games"
    response = requests.get(url)  # Realizar solicitud GET a la API
    juegos = response.json()  # Convertir la respuesta a formato JSON

    if query:
        # Filtrar juegos por título que contenga la query, ignorando mayúsculas y minúsculas
        juegos_filtrados = [juego for juego in juegos if query.lower() in juego['title'].lower()]
    else:
        juegos_filtrados = juegos[:12]  # Limitar a 12 juegos si no hay query

    categorias = Categoria.objects.all()
    for juego in juegos_filtrados:
        numero_aleatorio = random.randint(10000, 59990)
        juego['precio'] = "{:,}".format(numero_aleatorio).replace(",", ".")  # Agregar clave 'precio' a cada juego

    return render(request, 'juegos/index.html', {'juegos': juegos_filtrados, 'categorias': categorias})

def vista_protegida(request):
    return render(request, 'juegos/protegida.html')

@login_required
def vista_protegida(request):
    return render(request, 'juegos/protegida.html')

@login_required
def listar_productos(request):
    productos = Categoria.objects.all()
    return render(request, 'juegos/listar.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form= ProductoForm()
        return render (request, 'juegos/crear.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto=get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'juegos/editar.html', {'form':form})
    
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'juegos/eliminar.html', {'producto': producto})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("listar_productos")
    else:
        form = UserCreationForm()
    return render(request, 'juegos/registro.html', {'form': form})

def get_success_url(self):
    if self.request.user.is_superuser:
        return '/admin/' #puedes redirigir a cualquiera otra pagina especial para superusuario
    return redirect('listar_productos')

@login_required
def perfil_usuario(request):
    if request.user.is_superuser:
        usuarios = User.objects.all()
    else:
        usuarios = None

    context = {
        'user': request.user,
        'usuarios':usuarios,
    }

    return render(request, 'juegos/perfil.html', context)

def agregar_al_carrito(request, producto_id):
    # Obtener el producto o devolver un error 404 si no existe
    url = f"https://www.freetogame.com/api/game?id={producto_id}"
    response = requests.get(url) #realizar solicitud Get a la Api
    producto = response.json()  #convertir la respuesta a formato Json
    numero_aleatorio = random.randint(10000, 59990)
    producto['precio'] = "{:,}".format(numero_aleatorio).replace(",", ".")
    
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    # Si el producto ya está en el carrito, incrementar la cantidad
    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += 1
    else:
        # Agregar el producto al carrito con la cantidad inicial de 1
        carrito[producto_id] = {
            'nombre': producto['title'],
            'precio': float(producto['precio']),  # Convertimos a float para evitar problemas de JSON
            'cantidad': 1,
        }
    
    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito
    
    # Redirigir a la lista de productos o a la vista del carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0
    for producto_id, item in carrito.items():
        item['total'] = item['precio'] * item['cantidad']
        total += total + item['total']
            
    return render(request, 'juegos/ver_carrito.html', {'carrito': carrito, 'total': total})

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    # Si el producto está en el carrito, eliminarlo
    if producto_id in carrito:
        del carrito[producto_id]
    
    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('ver_carrito')

def vaciar_carrito(request):
    # Vaciar el carrito en la sesión
    request.session['carrito'] = {}
    
    return redirect('ver_carrito')

def actualizar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})
        
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            if nueva_cantidad > 0:
                carrito[producto_id_str]['cantidad'] = nueva_cantidad
            else:
                del carrito[producto_id_str]  # Eliminar el producto si la cantidad es 0
        
        request.session['carrito'] = carrito
        
    return redirect('ver_carrito')

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # Requiere que el usuario esté autenticado
def categorias_api(request, pk=None):
    # GET - Listar categorias o obtener uno en específico
    if request.method == 'GET':
        if pk:
            categoria = get_object_or_404(Categoria, pk=pk)
            serializer = CategoriaSerializer(categoria)
        else:
            categorias = Categoria.objects.all()
            serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    # POST - Crear un nuevo producto
    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT - Actualizar un producto existente
    elif request.method == 'PUT':
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE - Eliminar un categoria
    elif request.method == 'DELETE':
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def listar_categorias_juegos(request):
    url = "https://www.freetogame.com/api/games"
    response = requests.get(url) #realizar solicitud Get a la Api
    data = response.json()  #convertir la respuesta a formato Json
    
    categorias = data['categories'] #Obtener categorias o generos de los juegos
    
    return render (request, 'juegos/listar_categorias_juegos.html',{'categorias': categorias})






