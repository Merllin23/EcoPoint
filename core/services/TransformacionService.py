from core.models import Material, ProcesoTransformacion
from django.utils import timezone

ETAPAS_MATERIALES = {
    "Plástico": [
        "Clasificación", "Trituración", "Lavado", "Secado",
        "Fundido", "Peletizado", "Almacenado"
    ],
    "Vidrio": [
        "Separación por color", "Limpieza superficial", "Molienda",
        "Fundición", "Moldeado", "Almacenado"
    ],
    "Cartón": [
        "Clasificación", "Trituración", "Pulpeado",
        "Refinado", "Prensado", "Secado", "Almacenado"
    ],
}

ETAPAS_DEFAULT = [
    "Clasificación", "Trituración", "Lavado",
    "Fundido", "Prensado", "Almacenado"
]

MENSAJES_ETAPAS = {
    "Clasificación": "Separamos el material para asegurar un reciclaje eficiente.",
    "Trituración": "El material se reduce a fragmentos pequeños.",
    "Lavado": "Limpiamos el material para eliminar impurezas.",
    "Secado": "El material se seca antes de continuar.",
    "Fundido": "El material se derrite para ser reutilizado.",
    "Peletizado": "El plástico se convierte en pellets.",
    "Prensado": "El material se comprime.",
    "Pulpeado": "El cartón se convierte en pasta.",
    "Refinado": "La pasta es mejorada para reutilización.",
    "Molienda": "El vidrio se tritura hasta obtener calcín.",
    "Moldeado": "El vidrio toma nuevas formas.",
    "Limpieza superficial": "Se elimina suciedad básica del vidrio.",
    "Separación por color": "Se clasifica el vidrio por color.",
    "Almacenado": "Material reciclado y listo.",
}

def obtener_etapas(material):
    return ETAPAS_MATERIALES.get(material.tipo, ETAPAS_DEFAULT)

def etapa_actual(material):
    ultimo = material.procesotransformacion_set.order_by("-fecha_registro").first()
    return ultimo.etapa if ultimo else None


class TransformacionService:

    def listar_materiales(self, usuario):
        if usuario.rol == "admin":
            return Material.objects.all().order_by('-id_material')
        return Material.objects.filter(usuario=usuario).order_by('-id_material')

    def obtener_mensaje(self, etapa):
        return MENSAJES_ETAPAS.get(etapa, "")

    def avanzar_etapa(self, material_id):
        try:
            material = Material.objects.get(id_material=material_id)
            etapas = obtener_etapas(material)
            actual = etapa_actual(material)

            if actual is None:
                siguiente = etapas[0]
            else:
                pos = etapas.index(actual)
                if pos + 1 >= len(etapas):
                    return False, "El material ya completó todas las etapas."
                siguiente = etapas[pos + 1]

            ProcesoTransformacion.objects.create(
                material=material,
                etapa=siguiente,
                fecha_registro=timezone.now()
            )

            return True, f"{material.tipo} avanzó a '{siguiente}'."

        except Exception as e:
            return False, str(e)
