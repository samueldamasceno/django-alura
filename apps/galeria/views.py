from django.shortcuts import render, get_object_or_404, redirect
from apps.galeria.models import Fotografia
from django.contrib import messages
from apps.galeria.forms import FotografiaForm

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True)
    return render(request, 'galeria/index.html', {"fotografias": fotografias})

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    imagem_url = cloudinary_url(fotografia.cloudinary_public_id, width=800, height=800, crop="fill")[0]
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia, 'imagem_url': imagem_url})

def buscar(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True)

    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)

    return render(request, "galeria/index.html", {"fotografias": fotografias})

def nova_imagem(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    form = FotografiaForm()
    
    if request.method == 'POST':
        form = FotografiaForm(request.POST, request.FILES)
        
        if form.is_valid():
            imagem = upload(
                request.FILES['foto'].file,
                public_id=f"galeria/{form.cleaned_data['nome']}",
                crop="scale",
                width=800,
                height=600
            )

            form.instance.cloudinary_public_id = imagem['public_id']

            form.save()
            messages.success(request, 'Fotografia cadastrada com sucesso')
            return redirect('index')
    
    return render(request, 'galeria/nova_imagem.html', {'form': form})

def editar_imagem(request, foto_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    fotografia = get_object_or_404(Fotografia, id=foto_id)
    form = FotografiaForm(instance=fotografia)

    if request.method == 'POST':
        form = FotografiaForm(request.POST, request.FILES, instance=fotografia)
        
        if form.is_valid():
            if 'foto' in request.FILES:
                imagem = upload(
                    request.FILES['foto'].file,
                    public_id=f"galeria/{form.cleaned_data['nome']}",
                    crop="scale",
                    width=800,
                    height=800
                )

                form.instance.cloudinary_public_id = imagem['public_id']
            
            form.save()
            messages.success(request, 'Fotografia editada com sucesso')
            return redirect('index')
    
    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})

def deletar_imagem(request, foto_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    fotografia = Fotografia.objects.get(id=foto_id)
    fotografia.delete()
    messages.success(request, 'Foto deletada com sucesso')
    
    return redirect('index')

def filtro(request, categoria):
    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True, categoria=categoria)
    return render(request, 'galeria/index.html', {"fotografias": fotografias})