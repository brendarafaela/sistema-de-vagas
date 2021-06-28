from django.shortcuts import render, redirect

from vagas.base.forms import UsuarioForm, UsuarioFormCadastro, CandidatoForm, VagaForm
from vagas.base.models import Usuario, Vaga, UsuarioVaga
from django.db.models.functions import TruncMonth
from django.db.models import Count


def login(requisicao):
    if requisicao.method == 'GET':
        try:
            usuario_id = requisicao.session['usuario_id']
            usuario_tipo = requisicao.session['usuario_tipo']

            return redirect('/vagas/listar')
        except KeyError:
            return render(requisicao, 'base/login.html')

    if requisicao.method == 'POST':
        formulario = UsuarioForm(requisicao.POST)
        email = requisicao.POST['email']
        senha = requisicao.POST['senha']

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)

            if formulario.is_valid():
                requisicao.session['usuario_id'] = usuario.id
                requisicao.session['usuario_tipo'] = usuario.tipoDeUsuario
                requisicao.session['usuario_nome'] = usuario.nome

                return redirect('/vagas/listar')
            else:
                contexto = {'formulario': formulario}
                return render(requisicao, 'base/login.html', contexto)

        except Usuario.DoesNotExist:
            contexto = {'erro': 'Usuário ou senha inválidos.'}
            return render(requisicao, 'base/login.html', contexto)

    return render(requisicao, 'base/login.html')


def cadastro(requisicao):
    if requisicao.method == 'GET':
        return render(requisicao, 'base/cadastro.html')

    if requisicao.method == 'POST':
        formulario = UsuarioFormCadastro(requisicao.POST)
        nome = requisicao.POST['nome']
        email = requisicao.POST['email']
        senha = requisicao.POST['senha']

        try:
            usuario = Usuario.objects.get(email=email)

            contexto = {'erro': 'Esse email já está sendo utilizado.'}
            return render(requisicao, 'base/cadastro.html', contexto)

        except Usuario.DoesNotExist:
            if formulario.is_valid():
                Usuario(nome=nome, email=email, senha=senha, tipoDeUsuario=1).save()
                contexto = {'sucesso': 'Cadastro realizado com sucesso.'}
                return render(requisicao, 'base/cadastro.html', contexto)
            else:
                contexto = {'formulario': formulario}
                return render(requisicao, 'base/cadastro.html', contexto)


def sair(requisicao):
    del requisicao.session['usuario_id']
    del requisicao.session['usuario_tipo']
    del requisicao.session['usuario_nome']

    return redirect('/login')


def vagas_listar(requisicao):
    # verificar se ainda tem sessao
    try:
        # tenta achar sessao de usuario
        usuario_id = requisicao.session['usuario_id']
        usuario_tipo = requisicao.session['usuario_tipo']
        usuario_nome = requisicao.session['usuario_nome']

        # ver se e admin
        if usuario_tipo != 0:
            return redirect('/login')

    except KeyError:
        # se nao achou joga pra tela de login
        return redirect('/login')
    # verificar se ainda tem sessao

    vagas = Vaga.objects.all().order_by('-dataCadastro')
    vagasCandidaturas = []

    for vaga in vagas:
        qtdCandidatos = UsuarioVaga.objects.filter(vaga=vaga).count()
        vagasCandidaturas.append(qtdCandidatos)

    contexto = {
        'vagas': vagas,
        'vagasCandidaturas': vagasCandidaturas,
        'usuario_nome': requisicao.session['usuario_nome'],
        'usuario_tipo': requisicao.session['usuario_tipo'],
        'vagas_candidaturas': vagas_candidaturas
    }

    return render(requisicao, 'base/vagas-listar.html', contexto)


def vagas_candidaturas(requisicao, id_vaga):
    # verificar se ainda tem sessao
    try:
        # tenta achar sessao de usuario
        usuario_id = requisicao.session['usuario_id']
        usuario_tipo = requisicao.session['usuario_tipo']
        usuario_nome = requisicao.session['usuario_nome']

        # ver se e admin
        if usuario_tipo != 0:
            return redirect('/login')

        candidaturas = UsuarioVaga.objects.filter(vaga=id_vaga)
        vaga = Vaga.objects.get(id=id_vaga)

        contexto = {
            'usuario_nome': requisicao.session['usuario_nome'],
            'candidaturas': candidaturas,
            'vaga': vaga
        }

        return render(requisicao, 'base/vagas-candidaturas.html', contexto)

    except KeyError:
        # se nao achou joga pra tela de login
        return redirect('/login')
    # verificar se ainda tem sessao


def vagas_candidatar(requisicao, id_vaga):
    # verificar se ainda tem sessao
    try:
        # tenta achar sessao de usuario
        usuario_id = requisicao.session['usuario_id']
        usuario_tipo = requisicao.session['usuario_tipo']
        vaga = Vaga.objects.get(id=id_vaga)

        if usuario_tipo != 1:
            return redirect('/login')

    except KeyError:
        # se nao achou joga pra tela de login
        return redirect('/login')
    # verificar se ainda tem sessao

    contexto = {
        'usuario_id': requisicao.session['usuario_id'],
        'usuario_nome': requisicao.session['usuario_nome'],
        'vaga': vaga,
        'id_vaga': id_vaga,
        'opcoesEscolaridade': [
            (0, 'Ensino Fundamental'),
            (1, 'Ensino médio'),
            (2, 'Tecnólogo'),
            (3, 'Ensino Superior'),
            (4, 'Pós / MBA / Mestrado'),
            (5, 'Doutorado'),
        ],
        'opcoesPretensao': [
            (0, 'Até 1.000'),
            (1, 'De 1.000 a 2.000'),
            (2, 'De 2.000 a 3.000'),
            (3, 'Acima de 3.000'),
        ]
    }

    # salvar o post
    if requisicao.method == 'POST':
        formulario = CandidatoForm(requisicao.POST)
        pretensaoSalario = requisicao.POST['pretensaoSalario']
        ultimaEscolaridade = requisicao.POST['ultimaEscolaridade']
        experiencia = requisicao.POST['experiencia']

        try:
            usuario = Usuario.objects.get(id=usuario_id)

            if formulario.is_valid():
                UsuarioVaga(usuario=usuario, vaga=vaga, pretensaoSalario=pretensaoSalario,
                            experiencia=experiencia, ultimaEscolaridade=ultimaEscolaridade).save()
                contexto['sucesso'] = 'Candidatura realizada com sucesso, entraremos em contato.'
            else:
                contexto['formulario'] = formulario
        except Usuario.DoesNotExist:
            contexto['erro'] = 'Usuário ou Vaga não encontrados.'
    # salvar o post

    return render(requisicao, 'base/vagas-candidatar.html', contexto)


def vagas_cadastrar(requisicao):
    # verificar se ainda tem sessao
    try:
        # tenta achar sessao de usuario
        usuario_id = requisicao.session['usuario_id']
        usuario_tipo = requisicao.session['usuario_tipo']
        usuario_nome = requisicao.session['usuario_nome']

        # ver se e admin
        if usuario_tipo != 0:
            return redirect('/login')

    except KeyError:
        # se nao achou joga pra tela de login
        return redirect('/login')
    # verificar se ainda tem sessao

    contexto = {
        'usuario_nome': requisicao.session['usuario_nome'],
        'opcoesEscolaridade': [
            (0, 'Ensino Fundamental'),
            (1, 'Ensino médio'),
            (2, 'Tecnólogo'),
            (3, 'Ensino Superior'),
            (4, 'Pós / MBA / Mestrado'),
            (5, 'Doutorado'),
        ],
        'opcoesPretensao': [
            (0, 'Até 1.000'),
            (1, 'De 1.000 a 2.000'),
            (2, 'De 2.000 a 3.000'),
            (3, 'Acima de 3.000'),
        ]
    }

    if requisicao.method == 'POST':
        formulario = VagaForm(requisicao.POST)
        nomeVaga = requisicao.POST['nomeVaga']
        requisitos = requisicao.POST['requisitos']
        faixaSalario = requisicao.POST['faixaSalario']
        escolaridadeMinima = requisicao.POST['escolaridadeMinima']

        try:
            if formulario.is_valid():
                Vaga(nomeVaga=nomeVaga, requisitos=requisitos,
                     faixaSalario=faixaSalario, escolaridadeMinima=escolaridadeMinima).save()
                contexto['sucesso'] = 'Vaga cadastrada com sucesso.'
            else:
                contexto['formulario'] = formulario

        except KeyError:
            contexto['erro'] = 'Erro ao tentar cadastrar vaga, tente novamente.'

    return render(requisicao, 'base/vagas-cadastrar.html', contexto)


def vagas_excluir(requisicao, id_vaga):
    # verificar se ainda tem sessao
    try:
        # tenta achar sessao de usuario
        usuario_tipo = requisicao.session['usuario_tipo']

        if usuario_tipo == 0:
            Vaga.objects.filter(id=id_vaga).delete()
            return redirect('/vagas/listar')
        else:
            return redirect('/vagas/listar')

    except KeyError:
        # se nao achou joga pra tela de login
        return redirect('/login')
    # verificar se ainda tem sessao


def vagas_editar(requisicao, id_vaga):
    # verificar se ainda tem sessao
    try:
        # tenta achar sessao de usuario
        usuario_id = requisicao.session['usuario_id']
        usuario_tipo = requisicao.session['usuario_tipo']
        usuario_nome = requisicao.session['usuario_nome']

        # ver se e admin
        if usuario_tipo != 0:
            return redirect('/login')

    except KeyError:
        # se nao achou joga pra tela de login
        return redirect('/login')
    # verificar se ainda tem sessao

    try:
        vaga = Vaga.objects.get(id=id_vaga)

    except Vaga.DoesNotExist:
        return redirect('/')

    contexto = {
        'vaga': vaga,
        'usuario_nome': requisicao.session['usuario_nome'],
        'opcoesEscolaridade': [
            (0, 'Ensino Fundamental'),
            (1, 'Ensino médio'),
            (2, 'Tecnólogo'),
            (3, 'Ensino Superior'),
            (4, 'Pós / MBA / Mestrado'),
            (5, 'Doutorado'),
        ],
        'opcoesPretensao': [
            (0, 'Até 1.000'),
            (1, 'De 1.000 a 2.000'),
            (2, 'De 2.000 a 3.000'),
            (3, 'Acima de 3.000'),
        ]
    }

    if requisicao.method == 'POST':
        formulario = VagaForm(requisicao.POST)
        nomeVaga = requisicao.POST['nomeVaga']
        requisitos = requisicao.POST['requisitos']
        faixaSalario = requisicao.POST['faixaSalario']
        escolaridadeMinima = requisicao.POST['escolaridadeMinima']

        try:
            if formulario.is_valid():
                vaga.__dict__.update(nomeVaga=nomeVaga, requisitos=requisitos,
                                     faixaSalario=faixaSalario, escolaridadeMinima=escolaridadeMinima)
                vaga.save()
                contexto['sucesso'] = 'Vaga atualizada com sucesso.'
            else:
                contexto['formulario'] = formulario

        except KeyError:
            contexto['erro'] = 'Erro ao tentar cadastrar vaga, tente novamente.'

    return render(requisicao, 'base/vagas-editar.html', contexto)


def vagas_relatorios(requisicao):
    # verificar se ainda tem sessao
    try:
        # tenta achar sessao de usuario
        usuario_id = requisicao.session['usuario_id']
        usuario_tipo = requisicao.session['usuario_tipo']
        usuario_nome = requisicao.session['usuario_nome']

        # ver se e admin
        if usuario_tipo != 0:
            return redirect('/login')

    except KeyError:
        # se nao achou joga pra tela de login
        return redirect('/login')
    # verificar se ainda tem sessao

    vagasCriadas = (Vaga.objects
                    .annotate(month=TruncMonth('dataCadastro'))
                    .values('month')
                    .annotate(c=Count('id'))
                    .values('month', 'c'))

    vagasAplicadas = (UsuarioVaga.objects
                      .annotate(month=TruncMonth('dataCadastro'))
                      .values('month')
                      .annotate(c=Count('id'))
                      .values('month', 'c'))

    contexto = {
        'vagasCriadas': vagasCriadas,
        'vagasAplicadas': vagasAplicadas,
        'usuario_nome': usuario_nome
    }

    return render(requisicao, 'base/vagas-relatorios.html', contexto)
