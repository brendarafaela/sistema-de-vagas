"""vagas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vagas.base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login),
    path('', views.login),
    path('sair', views.sair),
    path('cadastro', views.cadastro),
    path('vagas/listar', views.vagas_listar),
    path('vagas/cadastrar', views.vagas_cadastrar),
    path('vagas/relatorios', views.vagas_relatorios),
    path('vagas/excluir/<int:id_vaga>', views.vagas_excluir),
    path('vagas/candidatar/<int:id_vaga>', views.vagas_candidatar),
    path('vagas/candidaturas/<int:id_vaga>', views.vagas_candidaturas),
    path('vagas/editar/<int:id_vaga>', views.vagas_editar)
]
