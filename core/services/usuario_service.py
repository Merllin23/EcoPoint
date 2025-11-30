from core.models import Usuario
from django.contrib.auth.hashers import check_password, make_password

class UsuarioService:

    def autenticar(self, correo, contrasena):
        """Verifica si el usuario existe y la contraseña es correcta."""
        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return None
        
        if check_password(contrasena, usuario.contrasena):
            return usuario
        
        return None

    def crear_usuario(self, nombre, correo, contrasena):
        """Crea un usuario con contraseña encriptada."""
        return Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            contrasena=make_password(contrasena),
            rol="usuario"
        )
