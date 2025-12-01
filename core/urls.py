from django.urls import path
from django.shortcuts import redirect
from . import views
from core.views import reportes_view, exportar_reporte_csv

urlpatterns = [
    path('', lambda request: redirect('login')),  
    path('login/', views.login_view, name='login'),
    path('registrar/', views.registrar_material_view, name ='registrar'),
    path('panel-gestor/', views.panel_gestor_view, name='panel_gestor'),
    path('transformacion/', views.transformacion_view, name ='transformacion'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('estadisticas/', views.estadisticas_view, name='estadisticas'),

    #para exportar
    path('reportes/', reportes_view, name='reportes'),
    path('reportes/exportar/', exportar_reporte_csv, name='exportar_reporte_csv'),

]
