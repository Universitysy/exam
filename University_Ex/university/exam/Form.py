from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Override the username field to use email
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({'autofocus': True})

