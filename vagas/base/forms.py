from django.forms import ModelForm

from vagas.base.models import Usuario, UsuarioVaga, Vaga


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'senha']


class UsuarioFormCadastro(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha']


class CandidatoForm(ModelForm):
    class Meta:
        model = UsuarioVaga
        fields = ['pretensaoSalario', 'ultimaEscolaridade', 'experiencia']


class VagaForm(ModelForm):
    class Meta:
        model = Vaga
        fields = ['nomeVaga', 'requisitos', 'faixaSalario', 'escolaridadeMinima']