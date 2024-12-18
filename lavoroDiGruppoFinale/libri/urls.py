from django.urls import path
from . import views
from .views import CustomLoginView, change_password, elimina_libro
from django.contrib.auth.views import LogoutView
from .views import AuthView
 
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('aggiungi_libro/', views.aggiungi_libro, name='aggiungi_libro'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('register/', views.register, name='register'),
    path('miei_libri', views.miei_libri, name='miei_libri'),
    path('cambia-password/', views.change_password, name='change_password'),
    path('libro/elimina/<int:libro_id>/', elimina_libro, name='elimina_libro'),
]