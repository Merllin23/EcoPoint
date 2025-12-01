from core.models import Clasificacion, Usuario
from collections import defaultdict

class GestorService:

    def listar_pendientes(self):
        """Devuelve todos los materiales con clasificacion pendiente"""
        return Clasificacion.objects.filter(estado="Pendiente").select_related('material', 'material__usuario')

    def estadisticas_rapidas(self):
        """Calcula estadísticas rápidas"""
        import datetime
        hoy = datetime.date.today()
        registros_hoy = Clasificacion.objects.filter(
            fecha_registro__date=hoy
        )
        total_kg = sum([float(c.material.peso) for c in registros_hoy])
        nuevos = registros_hoy.count()
        return {"total_hoy": total_kg, "nuevos_registros": nuevos}

    def actualizar_estado(self, clasificacion_id, nuevo_estado, comentario=None):
        """Acepta o rechaza un registro y ajusta puntos del usuario"""
        try:
            clasificacion = Clasificacion.objects.get(id_clasificacion=clasificacion_id)
            usuario = clasificacion.material.usuario

            estado_anterior = clasificacion.estado

            # Ajustamos puntos según cambio de estado
            if estado_anterior != nuevo_estado:
                if estado_anterior == "Pendiente" and nuevo_estado == "Aceptada":
                    puntos = 5 if comentario else 10
                    usuario.puntos += puntos
                    usuario.save()
                elif estado_anterior == "Aceptada" and nuevo_estado == "Rechazada":
                    puntos = 5 if clasificacion.comentario_gestor else 10
                    usuario.puntos -= puntos
                    usuario.save()

            # Actualizar clasificación
            clasificacion.estado = nuevo_estado
            if comentario:
                clasificacion.comentario_gestor = comentario
            clasificacion.save()

            return True, None
        except Clasificacion.DoesNotExist:
            return False, "Clasificación no encontrada."
        
    
