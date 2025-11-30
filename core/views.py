from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario
from django.shortcuts import render, redirect
from django.contrib import messages
from core.services.usuario_service import UsuarioService

usuario_service = UsuarioService()

def login_view(request):
    if request.method == "POST":
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contraseña')

        usuario = usuario_service.autenticar(correo, contrasena)

        if usuario:
            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_rol'] = usuario.rol
            return redirect('dashboard')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('login')

    return render(request, 'core/login.html')


def register_view(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        contrasena2 = request.POST.get('password2')

        if contrasena != contrasena2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        # Verificar si existe
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Ese correo ya está registrado.")
            return redirect('register')

        # Crear usuario usando POO
        usuario_service.crear_usuario(nombre, correo, contrasena)

        messages.success(request, "Registro exitoso. ¡Ahora inicia sesión!")
        return redirect('login')

    return render(request, 'core/register.html')


def dashboard_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect('login')

    # Datos reales iniciales (por ahora todo en 0 porque no hay registros)
    user_points = usuario.puntos if hasattr(usuario, 'puntos') else 0
    user_rank = "-"  
    ultimos_registros = []  # aún no hay nada real
    impacto_kg = 0
    impacto_co2 = 0

    context = {
        'usuario': usuario,
        'user_points': user_points,
        'user_rank': user_rank,
        'ultimos_registros': ultimos_registros,
        'impacto_kg': impacto_kg,
        'impacto_co2': impacto_co2,
    }

    return render(request, 'core/dashboard.html', context)

def logout_view(request):
    request.session.flush()   # Borra toda la sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')
