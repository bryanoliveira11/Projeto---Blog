from django.forms import ModelForm
from .models import Comentario
import requests

class FormComentario(ModelForm):

    def clean(self):
        raw_data = self.data
        recaptcha_response = raw_data.get("g-recaptcha-response")
        
        if not recaptcha_response:
            self.add_error('comentario','Marque a Caixa "Não sou um Robô".')
            
        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data = {
                'secret':'6LcddEolAAAAAN7xco43XbY6gcHaL1vFNPRhA7vS',
                'response': recaptcha_response
            }
            ) 
        
        recaptcha_result = recaptcha_request.json()
        
        cleaned_data = self.cleaned_data
        nome = cleaned_data.get('nome_comentario')
        email = cleaned_data.get('email_comentario')
        comentario = cleaned_data.get('comentario')

        if len(nome) < 5:
            self.add_error('nome_comentario','Nome precisa ter mais que 5 caracteres')

    class Meta:
        model = Comentario
        fields = ('nome_comentario','email_comentario','comentario',)