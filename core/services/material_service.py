from core.models import Material, Clasificacion, Usuario
from datetime import datetime

class MaterialService:

    def registrar_material(self, usuario_id, tipo, sugerencia, observaciones, cantidad, peso, estado, foto=None):
        """
        Registra un material y su clasificación, sumando puntos al usuario.
        """

        # Obtener usuario
        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
        except Usuario.DoesNotExist:
            return None, "Usuario no encontrado"

        # Crear registro de material
        material = Material.objects.create(
            usuario=usuario,
            tipo=tipo,
            cantidad=cantidad,
            peso=peso,
            estado=estado,
            fotografia=foto.name if foto else None
            
        )
        

        # Crear clasificación asociada
        Clasificacion.objects.create(
            material=material,
            sugerencia=sugerencia,
            estado='Pendiente',
            fecha_registro=datetime.now()
        )

        # Sumar puntos al usuario
        usuario.puntos += 10
        usuario.save()

        return material, None
