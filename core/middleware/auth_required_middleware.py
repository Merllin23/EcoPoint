from django.shortcuts import redirect
from django.urls import resolve

class AuthRequiredMiddleware:
    PUBLIC_ROUTES = [
        'login',
        'register',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_route = resolve(request.path_info).url_name

        # Si la ruta NO está en las rutas públicas y NO hay sesión, redirige
        if current_route not in self.PUBLIC_ROUTES and not request.session.get('usuario_id'):
            return redirect('login')

        return self.get_response(request)

