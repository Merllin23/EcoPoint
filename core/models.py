from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, default="usuario")
    puntos = models.IntegerField(default=0)  

    class Meta:
        db_table = "usuario"
        managed = False  # Django no creará/modificará esta tabla


class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, db_column='id_usuario', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    fotografia = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "material"
        managed = False

    def __str__(self):
        return f"{self.tipo} - {self.usuario.nombre}"


class Clasificacion(models.Model):
    id_clasificacion = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, db_column='id_material', on_delete=models.CASCADE)
    sugerencia = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)  # Pendiente, Aceptada, Rechazada
    comentario_gestor = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField()  

    class Meta:
        db_table = "clasificacion"
        managed = False

    def __str__(self):
        return f"Clasificación de {self.material.tipo}"



class ProcesoTransformacion(models.Model):
    id_proceso = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, db_column='id_material', on_delete=models.CASCADE)
    etapa = models.CharField(max_length=50)  
    fecha_registro = models.DateTimeField()

    class Meta:
        db_table = "procesotransformacion"
        managed = False

    def __str__(self):
        return f"{self.etapa} - {self.material.tipo}"


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, db_column='id_usuario', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)  # Personal, Global
    fecha = models.DateTimeField()

    class Meta:
        db_table = "reporte"
        managed = False

    def __str__(self):
        return f"Reporte {self.tipo} de {self.usuario.nombre}"
    