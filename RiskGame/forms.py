from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=45)
    last_name = forms.CharField(max_length=45)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']
        help_texts = {
            'username': "<br />L'username può contenere lettere, numeri e @/./+/-/_ soltanto",
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "<br />La password non può essere troppo simile alle tue altre informazioni personali<br />" \
                                             "La password deve contenere almeno 8 caratteri<br />" \
                                             "La password non può essere interamente numerica<br />" \
                                             "La password non può essere comune"
        self.fields['password2'].help_text = "<br />Inserisci la stessa password, per verificare"
