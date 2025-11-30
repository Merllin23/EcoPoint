from django.contrib import admin
from .models import Usuario, Material, Clasificacion, ProcesoTransformacion, Reporte

admin.site.register(Usuario)
admin.site.register(Material)
admin.site.register(Clasificacion)
admin.site.register(ProcesoTransformacion)
admin.site.register(Reporte)
