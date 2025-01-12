from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Categoria
from .forms import PostForm
from django.core.paginator import Paginator

def inicio(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)  # Muestra 5 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/inicio.html', {'page_obj': page_obj})

def agregar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el nuevo post
            return redirect('inicio')  # Redirigir al inicio, o a donde prefieras
    else:
        form = PostForm()

    return render(request, 'blog/agregar_post.html', {'form': form})

def buscar_posts(request):
    buscar = request.GET.get('buscar', '')
    if buscar:
        posts = Post.objects.filter(titulo__icontains=buscar)
    else:
        posts = Post.objects.none()
    return render(request, 'blog/buscar_posts.html', {'posts': posts})

def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detalle_post.html', {'post': post})
