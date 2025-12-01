from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from core.models import Usuario, Material, Clasificacion
from core.services.usuario_service import UsuarioService
from core.services.material_service import MaterialService
from decimal import Decimal
from core.services.GestorService import GestorService
from core.services.TransformacionService import TransformacionService



usuario_service = UsuarioService()
material_service = MaterialService()
gestor_service = GestorService()
transformacion_service = TransformacionService()


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

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Ese correo ya está registrado.")
            return redirect('register')

        usuario_service.crear_usuario(nombre, correo, contrasena)
        messages.success(request, "Registro exitoso. ¡Ahora inicia sesión!")
        return redirect('login')

    return render(request, 'core/register.html')


def dashboard_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])

    # Últimos 5 registros del usuario
    ultimos_registros = Material.objects.filter(usuario=usuario).order_by('-id_material')[:5]

    for m in ultimos_registros:
        m.ultima_clasificacion = m.clasificacion_set.order_by('-fecha_registro').first()

    # Impacto total solo de materiales aceptados
    aceptados = Material.objects.filter(usuario=usuario, clasificacion__estado="Aceptada")
    impacto_kg = sum([float(m.peso) for m in aceptados])
    impacto_co2 = impacto_kg * 0.8  

    context = {
        'usuario': usuario,
        'user_points': usuario.puntos,      
        'ultimos_registros': ultimos_registros,
        'impacto_kg': impacto_kg,
        'impacto_co2': impacto_co2,
    }

    return render(request, 'core/dashboard.html', context)

def logout_view(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')


def registrar_material_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect('login')

    if request.GET.get('retroceder') == '1':
        request.session['paso_registro'] = 1
        return redirect('registrar')

    paso = request.session.get('paso_registro', 1)
    error = None

    if request.method == 'POST':
        if paso == 1:
            material = request.POST.get('material', '').strip()
            sugerencia = request.POST.get('sugerencia', '').strip()
            observaciones = request.POST.get('observaciones', '').strip()

            if not material or not sugerencia:
                error = "Material y sugerencia son obligatorios."
            else:
                request.session['material_seleccionado'] = material
                request.session['sugerencia'] = sugerencia
                request.session['observaciones'] = observaciones
                request.session['paso_registro'] = 2
                return redirect('registrar')

        elif paso == 2:
            cantidad = request.POST.get('cantidad')
            peso = request.POST.get('peso')
            estado = request.POST.get('estado')
            foto = request.FILES.get('foto', None)

            if not cantidad or not peso or not estado:
                error = "Cantidad, peso y estado son obligatorios."
            else:
                try:
                    cantidad = float(cantidad)
                    peso = float(peso)
                    if cantidad <= 0 or peso <= 0:
                        raise ValueError
                except:
                    error = "Cantidad y peso deben ser números mayores a 0."

            if not error:
                # Registramos usando el servicio y pasamos objeto Usuario
                material_obj, servicio_error = material_service.registrar_material(
                    usuario_id=usuario.id_usuario,
                    tipo=request.session.get('material_seleccionado', ''),
                    sugerencia=request.session.get('sugerencia', ''),
                    observaciones=request.session.get('observaciones', ''),
                    cantidad=cantidad,
                    peso=peso,
                    estado=estado,
                    foto=foto
                )

                if servicio_error:
                    error = servicio_error
                else:
                    for key in ['paso_registro', 'material_seleccionado', 'sugerencia', 'observaciones']:
                        request.session.pop(key, None)
                    messages.success(request, "Material registrado correctamente. ¡Has ganado 10 puntos!")
                    return redirect('dashboard')

    context = {
        'usuario': usuario,
        'paso': paso,
        'material_seleccionado': request.session.get('material_seleccionado', ''),
        'observaciones': request.session.get('observaciones', ''),
        'error': error
    }

    return render(request, 'core/registrar_material.html', context)


def panel_gestor_view(request):
    if 'usuario_rol' not in request.session or request.session['usuario_rol'] != 'admin':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('dashboard')

    usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])
    pendientes = gestor_service.listar_pendientes()
    stats = gestor_service.estadisticas_rapidas()

    if request.method == "POST":
        clasificacion_id = request.POST.get("clasificacion_id")
        accion = request.POST.get("accion")  # Aceptar / Rechazar
        comentario = request.POST.get("comentario", "").strip() or None

        nuevo_estado = "Aceptada" if accion == "Aceptar" else "Rechazada"
        ok, error = gestor_service.actualizar_estado(clasificacion_id, nuevo_estado, comentario)
        if ok:
            messages.success(request, f"Registro actualizado a {nuevo_estado}")
        else:
            messages.error(request, error)

        return redirect('panel_gestor')

    context = {
        "usuario": usuario,  
        "pendientes": pendientes,
        "stats": stats
    }
    return render(request, "core/panel_gestor.html", context)


from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Usuario
from core.services.TransformacionService import (
    TransformacionService,
    obtener_etapas,
    etapa_actual,
)

transformacion_service = TransformacionService()

def transformacion_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])
    materiales = transformacion_service.listar_materiales(usuario)

    if request.method == "POST" and usuario.rol == "admin":
        material_id = request.POST.get("material_id")
        ok, msg = transformacion_service.avanzar_etapa(material_id)

        if ok:
            messages.success(request, msg)
        else:
            messages.error(request, msg)

        return redirect("transformacion")


    materiales_proceso = 0
    materiales_completados = 0
    materiales_final = []

    for m in materiales:
        etapas_m = obtener_etapas(m)
        actual = etapa_actual(m)

        if actual is None:
            etapa_index = -1
        else:
            etapa_index = etapas_m.index(actual)

        porcentaje = int(((etapa_index + 1) / len(etapas_m)) * 100) if etapa_index >= 0 else 0

        # Estadísticas
        if actual == etapas_m[-1]:
            materiales_completados += 1
        else:
            materiales_proceso += 1

        # Mensaje educativo según etapa actual
        if actual is None:
            mensaje_etapa = "El proceso aún no comienza."
        else:
            mensaje_etapa = transformacion_service.obtener_mensaje(actual)

        materiales_final.append({
            "id_material": m.id_material,
            "tipo_material": m.tipo,
            "usuario": m.usuario,
            "porcentaje": porcentaje,
            "etapa_actual": etapa_index,
            "etapa_actual_nombre": actual if actual else "No iniciado",
            "mensaje_etapa": mensaje_etapa,
            "etapas": etapas_m,
        })

    context = {
        "usuario": usuario,
        "materiales": materiales_final,
        "stats": {
            "materiales_proceso": materiales_proceso,
            "materiales_completados": materiales_completados
        }
    }

    return render(request, "core/transformacion.html", context)


from django.shortcuts import render, redirect
from django.db.models import Sum
from core.models import Material, Usuario
import random

def estadisticas_view(request):
    # Verificar sesión
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id_usuario=usuario_id)

    materiales = Material.objects.filter(usuario_id=usuario_id)

    # Total reciclado
    total_kg = materiales.aggregate(total=Sum("peso"))["total"] or 0

    # === AGRUPACIÓN BONITA DE TIPOS ===
    MAPEO = {
        "PET1": "Plástico",
        "PET2": "Plástico",
        "PET3": "Plástico",
        "Plástico": "Plástico",
        "Plastico": "Plástico",
        "platico": "Plástico",
        "Plastico mixto": "Plástico",

        "Carton": "Cartón",
        "Cartón": "Cartón",

        "Vidrio": "Vidrio",

    }

    # Convertir a una lista limpia agrupada
    materiales_limpios = []

    for item in materiales.values("tipo", "peso"):
        tipo_original = item["tipo"]
        categoria = MAPEO.get(tipo_original, tipo_original)  

        materiales_limpios.append({
            "categoria": categoria,
            "peso": item["peso"]
        })

    # Agrupar suma por categoría
    distribucion = {}
    for m in materiales_limpios:
        cat = m["categoria"]
        distribucion[cat] = distribucion.get(cat, 0) + m["peso"]

    # Convertir a lista para el template
    distribucion_final = [
        {"categoria": cat, "kg": round(peso, 2)}
        for cat, peso in distribucion.items()
    ]

    # Consejos dinámicos
    consejos = [
        "Separa plásticos por tipo para facilitar su reciclaje.",
        "Lava los envases antes de reciclarlos.",
        "Aplasta botellas y latas para ahorrar espacio.",
        "Reutiliza frascos de vidrio antes de reciclarlos.",
        "Reduce el uso de plástico de un solo uso."
    ]

    contexto = {
        "usuario": usuario,
        "stats": {
            "total_kg": round(total_kg, 2),
            "puntos": usuario.puntos,
            "distribucion": distribucion_final
        },
        "consejo": random.choice(consejos)
    }

    return render(request, "core/estadisticas.html", contexto)
