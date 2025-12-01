from core.models import Material, Clasificacion, Usuario
from datetime import datetime
from decimal import Decimal

class MaterialService:

    def registrar_material(self, usuario_id, tipo, sugerencia, observaciones, cantidad, peso, estado, foto=None):
        """
        Registra un material y su clasificación, sumando puntos al usuario.
        """
        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
        except Usuario.DoesNotExist:
            return None, "Usuario no encontrado"

        # Crear registro de material
        material = Material.objects.create(
            usuario=usuario,
            tipo=tipo,
            cantidad=Decimal(cantidad),
            peso=Decimal(peso),
            estado=estado,
            fotografia=foto.name if foto else None
        )

        Clasificacion.objects.create(
            material=material,
            sugerencia=sugerencia,
            estado='Pendiente',
            fecha_registro=datetime.now()
        )

        # Sumar puntos al usuario (solo por registrar)
        usuario.puntos += 10
        usuario.save()

        return material, None
