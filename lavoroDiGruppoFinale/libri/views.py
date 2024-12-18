from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Q
from .models import Libri, UserRegistrationForm
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
 
 
def homepage(request):
  context = {}
  if request.user.is_authenticated:
    context['username'] = request.user.username
  return render(request, 'homepage.html', context)
 
 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('homepage')  
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
 
class CustomLoginView(LoginView):
  template_name= 'auth_page.html' #template per login
  def get_success_url(self):
     return reverse('homepage')
 
@login_required        #aggiunge libro solo se utente è autenticato
def aggiungi_libro(request):
    if request.method == 'POST':
        titolo = request.POST.get('titolo')
        autore = request.POST.get('autore')
        genere = request.POST.get('genere')
        anno_pubblicazione = request.POST.get('anno_pubblicazione')
 
        if not titolo:
            return HttpResponse("Il titolo non può essere vuoto", status = 400)
        if not anno_pubblicazione:
            anno_pubblicazione = None
 
        nuovo_libro = Libri(  # Crea una nuova istanza del database Libri FUNZIONAAAAA
            titolo=titolo,
            autore=autore,
            genere=genere,
            anno_pubblicazione=anno_pubblicazione,
            utente=request.user
        )
        nuovo_libro.save()
        messages.success(request, "Libro aggiunto con successo")
        return redirect('homepage')
    return redirect('homepage')
 
def elimina_libro(request, libro_id):
    libro = get_object_or_404(Libri, id=libro_id, utente=request.user)
    libro.delete()
    messages.success(request, "Libro eliminato con successo.")
    return redirect('miei_libri')
 
@login_required
def miei_libri(request):
    libri = Libri.objects.filter(utente=request.user)    
    query=request.GET.get('q', '')
    if query:
        libri = libri.filter(Q(titolo__icontains=query) | Q(autore__icontains=query))
   
    libri = libri.order_by('titolo')
    paginator = Paginator(libri, 10)  
    page_number = request.GET.get('page')
    libri_paginati = paginator.get_page(page_number)
    return render(request, 'miei_libri.html', {'libri': libri_paginati, 'query': query})
 
class AuthView(View):
    def get(self, request):
        return render(request, 'auth_page.html')
 
    def post(self, request):
        if 'login' in request.POST:  # Gestione login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
 
            if user is not None:
                login(request, user)
                messages.success(request, "Login effettuato con successo!")
                return redirect('homepage')  # Reindirizza alla homepage
            else:
                messages.error(request, "Credenziali non valide.")
                return render(request, 'auth_page.html', {'login_error': 'Credenziali non valide.'})
 
        elif 'register' in request.POST:  # Controlla se è un tentativo di registrazione
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
 
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registrazione avvenuta con successo.")
                return redirect('login')  
            except Exception as e:
                messages.error(request, f"Errore durante la registrazione: {str(e)}")
                return render(request, 'auth_page.html')
           
@login_required
def change_password(request):
    error_message = None
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # mantiene l'utente loggato
            messages.success(request, 'La tua password è stata cambiata con successo!')
            return redirect('homepage')  # Reindirizza alla homepage
        else:
            return render(request, 'registration/cambio_pass.html', {
                'form': form,
                'error_message': 'Ci sono stati degli errori nel cambiamento della password.'
            })
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/cambio_pass.html', {'form': form})