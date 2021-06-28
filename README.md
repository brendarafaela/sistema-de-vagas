# Sistema de Vagas

## Para utilizar necessário seguir os passos abaixo:

### Primeiro Passo

Com o Python 3 e o PIP instalado, instalar o Django:
`pip install -r requirements.txt`

### Segundo Passo

Rodar o migrate do Django, para criação das tabelas `python manage.py migrate`

### Terceiro Passo

Criar um superuser (este para criar um usuário do tipo ADMIN, usuário que pode cadastrar vagas).
`python manage.py createsuperuser`

### Quarto Passo

Caso precise criar um usuário ADMIN (para criar vagas), entrar no admin do Django 
http://127.0.0.1:8000/admin/ com os dados criados no passo anterior, e depois ir no módulo BASE/Usuários e criar um usuário com o TipoDeUsuario ADMIN.

* Caso seja um usuário comum (candidato) realizar o cadastro pelo link raiz http://127.0.0.1:8000/
    * Todo usuário comum pode ser admin e vice-versa, desde que seja atualizado no ADMIN do Django
    
### Quinto e Último Passo

Utilizar o sistema, após criar a conta realizar o login e usar as funcionalidades.
* Listar Vagas
    * Lista as vagas cadastradas no sistema
        * Caso o usuário seja ADMIN pode editar ou excluir as vagas 
          e também visualizar a quantidade de candidatos por vagas,
          clicando nos candidatos por vaga poderá visualizar todos os dados de cada candidato,
          caso seja apenas candidato pode se candidatar
    
* Cadastrar Vaga
    * Cadastra as vagas no sistema
    
* Editar Vaga
    * Edita as vagas cadastradas no sistema
    
* Candidatar na Vaga
    * Usuario é vinculado a vaga, como um candidato
    
* Relatórios
    * Traz os Relatórios de Vagas criadas por mês e Candidatos recebidos por mês