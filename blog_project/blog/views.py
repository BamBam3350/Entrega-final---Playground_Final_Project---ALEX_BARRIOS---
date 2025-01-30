from .models import Page, UserProfile
from .forms import UserProfileForm, ProfileForm, SignUpForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  

def page_list(request):
    pages = Page.objects.all() 
    return render(request, 'blog/page_list.html', {'pages': pages})

def user_profile(request, username):
    user_profile = UserProfile.objects.get(user__username=username) 
    return render(request, 'blog/user_profile.html', {'user_profile': user_profile})

class HomeView(TemplateView):
    template_name = 'blog/home.html' 

class AboutView(TemplateView):
    template_name = 'blog/about.html' 

class PageListView(ListView):
    model = Page
    template_name = 'blog/page_list.html'  
    context_object_name = 'pages' 

    def get_queryset(self):
        queryset = super().get_queryset()
        if not queryset.exists():
            self.extra_context = {'message': "No hay páginas aún."}
        return queryset

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/page_detail.html'  
    context_object_name = 'page'  

class CreatePageView(LoginRequiredMixin, CreateView):
    model = Page
    template_name = 'blog/create_page.html' 
    fields = ['title', 'content', 'image']  

    def get_success_url(self):
        return reverse_lazy('blog:page_list')  

class UpdatePageView(LoginRequiredMixin, UpdateView):
    model = Page
    template_name = 'blog/update_page.html'  
    fields = ['title', 'content', 'image']

    def get_success_url(self):
        return reverse_lazy('blog:page_list')  

class DeletePageView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = 'blog/delete_page.html'  

    def get_success_url(self):
        return reverse_lazy('blog:page_list')  

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('blog:home')  

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "¡Te has registrado correctamente!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Hubo un error con el formulario.")
        return response

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog:home') 
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")  
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('blog:home') 

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('blog:profile') 
        else:
            messages.error(request, "Hubo un error al guardar los cambios.") 
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=user_profile)

    return render(request, 'blog/profile.html', {'user_form': user_form, 'profile_form': profile_form})
