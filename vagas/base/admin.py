from django.contrib import admin

from vagas.base.models import Usuario, Vaga, UsuarioVaga


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'dataCadastro')


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('nomeVaga', 'dataCadastro')


@admin.register(UsuarioVaga)
class UsuarioVagaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vaga', 'dataCadastro')

