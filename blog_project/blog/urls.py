from django.urls import path
from . import views
from .views import HomeView, AboutView, PageListView, PageDetailView, CreatePageView, UpdatePageView, DeletePageView, SignUpView, login_view, logout_view, profile_view

app_name = 'blog' 

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  
    path('about/', AboutView.as_view(), name='about'),  

    
    path('pages/create/', CreatePageView.as_view(), name='create_page'),  
    path('pages/', PageListView.as_view(), name='page_list'),  
    path('pages/<slug:slug>/', PageDetailView.as_view(), name='page_detail'),  
    path('pages/<slug:slug>/edit/', UpdatePageView.as_view(), name='update_page'),  
    path('pages/<slug:slug>/delete/', DeletePageView.as_view(), name='delete_page'),  

    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),  
    path('profile/<str:username>/', views.user_profile, name='user_profile'),  
]
