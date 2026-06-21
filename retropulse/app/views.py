from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Producto

def home(request):
    """Landing Page con los productos destacados más recientes."""
    # Cargamos las últimas 3 adiciones de productos destacados
    destacados = Producto.objects.all().order_by('-cod_producto')[:3]
    return render(request, 'store/home.html', {'destacados': destacados})

def catalog(request):
    """Catálogo General con filtros basados en el campo 'tipo'."""
    productos = Producto.objects.all()
    tipo_filtro = request.GET.get('tipo')
    
    if tipo_filtro:
        try:
            # Filtramos estrictamente por el entero del tipo de producto
            productos = productos.filter(tipo=int(tipo_filtro))
        except ValueError:
            pass

    context = {
        'productos': productos,
        'tipo_actual': tipo_filtro,
    }
    return render(request, 'store/catalog.html', context)

def product_detail(request, cod_producto):
    """Detalle técnico del producto y control de adición por lote."""
    producto = get_object_or_404(Producto, cod_producto=cod_producto)
    return render(request, 'store/detail.html', {'producto': producto})

def about(request):
    """Sección Institucional (Acerca de Nosotros)."""
    return render(request, 'store/about.html')

def cart_detail(request):
    """Vista del Carrito de Compras del cliente."""
    return render(request, 'store/cart.html')

def auth_view(request):
    """Controlador unificado de Autenticación (Login e Inscripción)."""
    if request.user.is_authenticated:
        return redirect('store:home')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Flujo 1: Inicio de Sesión
        if action == 'login':
            user_in = request.POST.get('username')
            pass_in = request.POST.get('password')
            user = authenticate(request, username=user_in, password=pass_in)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido de vuelta, {user.username}!")
                # Redirección dinámica si el usuario venía desde el carrito
                next_url = request.GET.get('next', 'store:home')
                return redirect(next_url)
            else:
                messages.error(request, "Credenciales incorrectas de acceso. Inténtalo de nuevo.")
                
        # Flujo 2: Registro de nuevo usuario
        elif action == 'signup':
            user_in = request.POST.get('username')
            email_in = request.POST.get('email')
            pass_in = request.POST.get('password')
            
            if User.objects.filter(username=user_in).exists():
                messages.error(request, "Este nombre de usuario ya se encuentra registrado.")
            else:
                user = User.objects.create_user(username=user_in, email=email_in, password=pass_in)
                login(request, user)
                messages.success(request, "Cuenta creada con éxito. ¡Bienvenido a RetroPulse Vault!")
                return redirect('store:home')
                
    return render(request, 'store/auth.html')

def logout_view(request):
    """Finaliza la sesión actual."""
    logout(request)
    messages.info(request, "Has cerrado sesión de forma segura.")
    return redirect('store:home')

# Restricción exclusiva para staff/administradores de Django
@user_passes_test(lambda u: u.is_staff, login_url='store:login')
def db_inspector(request):
    """Inspector de Base de Datos y simulación ORM interactiva."""
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        # Procesamiento del formulario de inserción (soporta datos binarios request.FILES)
        try:
            tipo = int(request.POST.get('tipo'))
            nombre = request.POST.get('nombre')
            cantidad = int(request.POST.get('cantidad_productos'))
            precio = float(request.POST.get('precio_unitario'))
            descripcion = request.POST.get('descripcion')
            imagen = request.POST.get('imagen') 

            # Creación del registro en base de datos mediante ORM
            nuevo_producto = Producto.objects.create(
                tipo=tipo,
                nombre=nombre,
                cantidad_productos=cantidad,
                precio_unitario=precio,
                descripcion=descripcion,
                imagen=imagen
            )
            
                
            messages.success(request, f"Producto '{nombre}' insertado en la base de datos con el código {nuevo_producto.cod_producto}.")
            return redirect('store:db_inspector')
        except Exception as e:
            messages.error(request, f"Error al insertar el registro: {str(e)}")

    return render(request, 'store/db_inspector.html', {'productos': productos})


@user_passes_test(lambda u: u.is_staff, login_url='store:login')
def eliminar_producto(request, cod_producto):
    """Elimina de forma segura un producto de la base de datos y su imagen del disco."""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, cod_producto=cod_producto)
        nombre_producto = producto.nombre
        
            
        # Borrado del registro en el ORM de Django
        producto.delete()
        
        messages.success(request, f"El producto '{nombre_producto}' ha sido eliminado con éxito de la base de datos.")
    else:
        messages.error(request, "Método de petición no permitido para esta acción.")
        
    return redirect('store:db_inspector')
