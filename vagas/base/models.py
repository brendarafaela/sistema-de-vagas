from django.db import models
from django.db.models import Func


class Usuario(models.Model):
    nome = models.CharField(max_length=40, default="")
    email = models.EmailField()
    senha = models.CharField(max_length=20)
    tipoDeUsuario = models.IntegerField(choices=[
        (0, 'ADMIN'),
        (1, 'USER'),
    ])
    dataCadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Vaga(models.Model):
    nomeVaga = models.CharField(max_length=40)
    requisitos = models.TextField(default="")
    faixaSalario = models.IntegerField(choices=[
        (0, 'Até 1.000'),
        (1, 'De 1.000 a 2.000'),
        (2, 'De 2.000 a 3.000'),
        (3, 'Acima de 3.000'),
    ])
    escolaridadeMinima = models.IntegerField(choices=[
        (0, 'Ensino Fundamental'),
        (1, 'Ensino médio'),
        (2, 'Tecnólogo'),
        (3, 'Ensino Superior'),
        (4, 'Pós / MBA / Mestrado'),
        (5, 'Doutorado'),
    ])
    dataCadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nomeVaga


class UsuarioVaga(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    pretensaoSalario = models.IntegerField(choices=[
        (0, 'Até 1.000'),
        (1, 'De 1.000 a 2.000'),
        (2, 'De 2.000 a 3.000'),
        (3, 'Acima de 3.000'),
    ])
    experiencia = models.TextField(default="")
    ultimaEscolaridade = models.IntegerField(choices=[
        (0, 'Ensino Fundamental'),
        (1, 'Ensino médio'),
        (2, 'Tecnólogo'),
        (3, 'Ensino Superior'),
        (4, 'Pós / MBA / Mestrado'),
        (5, 'Doutorado'),
    ])
    dataCadastro = models.DateTimeField(auto_now_add=True)
