from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, default="usuario")

    class Meta:
        db_table = "usuario"


class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    fotografia = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.usuario.nombre}"


class Clasificacion(models.Model):
    id_clasificacion = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    sugerencia = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)  # Pendiente, Confirmada, Corregida

    def __str__(self):
        return f"Clasificación de {self.material.tipo}"


class ProcesoTransformacion(models.Model):
    id_proceso = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    etapa = models.CharField(max_length=50)  
    fecha_registro = models.DateTimeField()

    def __str__(self):
        return f"{self.etapa} - {self.material.tipo}"


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)  # Personal, Global
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Reporte {self.tipo} de {self.usuario.nombre}"
