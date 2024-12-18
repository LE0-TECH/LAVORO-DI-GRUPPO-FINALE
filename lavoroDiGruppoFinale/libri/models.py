from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Libri(models.Model):
    titolo = models.CharField(max_length=200, verbose_name="Titolo", null=False, blank=False)
    autore = models.CharField(max_length=100, verbose_name="Autore", null=False, blank=False)
    genere= models.CharField(max_length=50, verbose_name="Genere", blank= True, null=True)
    anno_pubblicazione= models.IntegerField(verbose_name="Anno di pubblicazione", blank=True, null=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('titolo', 'autore')
    
    def __str__(self):
        return self.titolo

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels ={
            'username': 'Nome utente',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Conferma password',
        }