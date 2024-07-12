from django.shortcuts import render, redirect
from apps.usuarios.forms import LoginForm, CadastroForm
from django.contrib import auth,  messages
from django.contrib.auth.models import User
from django.contrib.auth import logout

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()
            
            usuario = auth.authenticate(
                request,
                username=nome,
                password=senha
            )

            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f'{nome} foi logado com sucesso!')
                return redirect('index')
            else:
                messages.error(request, 'Erro ao fazer login')
                return redirect('login')

    return render(request, 'usuarios/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Você foi deslogado com sucesso!')
    return redirect('login')

def cadastro(request):
    form = CadastroForm()

    if request.method == 'POST':
        form = CadastroForm(request.POST)
    
        if form.is_valid():
            if form['senha_1'].value() != form['senha_2'].value():
                messages.error(request, 'As senhas não são iguais')
                return redirect('cadastro')
            
            nome = form['nome_cadastro'].value()
            email = form['email'].value()
            senha = form['senha_1'].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Esse nome de usuário já existe')
                return redirect('cadastro')
            
            novo_usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )

            novo_usuario.save()
            messages.success(request, f'{nome} foi cadastrado com sucesso!')
            return redirect('login')


    return render(request, 'usuarios/cadastro.html', {'form': form})
