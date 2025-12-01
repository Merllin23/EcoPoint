from core.models import Clasificacion, Usuario

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
        """Acepta o rechaza un registro y ajusta puntos"""
        try:
            clasificacion = Clasificacion.objects.get(id_clasificacion=clasificacion_id)
            usuario = clasificacion.material.usuario

            # Ajustamos puntos solo si cambia el estado
            if clasificacion.estado != nuevo_estado:
                # Si se acepta ahora, sumamos puntos
                if nuevo_estado == "Aceptada":
                    puntos = 5 if comentario else 10
                    usuario.puntos += puntos
                # Si se rechaza después de haber sido aceptada, quitamos los puntos
                elif nuevo_estado == "Rechazada" and clasificacion.estado == "Aceptada":
                    puntos = 5 if clasificacion.comentario_gestor else 10
                    usuario.puntos -= puntos
                usuario.save()

            clasificacion.estado = nuevo_estado
            if comentario:
                clasificacion.comentario_gestor = comentario
            clasificacion.save()

            return True, None
        except Clasificacion.DoesNotExist:
            return False, "Clasificación no encontrada."
