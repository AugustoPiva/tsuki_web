from flatpickr import DatePickerInput
from django import forms
from .models import Pedidos,Tiposdegastos,Gastos,Clientes
# ,UserProfileInfo
from datetime import datetime,date
from dal import autocomplete
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','password')

class FormularioNuevoPedido(forms.ModelForm):
    client =forms.ModelChoiceField(
    queryset=Clientes.objects.all(),
    widget=autocomplete.ModelSelect2(attrs={'placeholder':'Nuevo gasto...'}))
    class Meta:
        model = Pedidos
        fields =  ['fecha','client','comentario']
        widgets = {
            'fecha': DatePickerInput(options = {"disableMobile": "true"},attrs={'stlye':'margin-top:20px;'}),
            'comentario':forms.Textarea(attrs={'rows':5}),
        }

class Fecha(forms.Form):
    dia= forms.DateField(widget=DatePickerInput(options = {"disableMobile": "true"}))
    # options={"dateFormat":""}


class Filtrargastos(forms.Form):
    seleccionar_gasto = forms.ModelChoiceField(
        queryset=Tiposdegastos.objects.all(),
        widget=autocomplete.ModelSelect2(attrs={'placeholder':'Nuevo gasto...'}))

class Nuevocliente(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre_apellido']
        widgets = {
        'nombre_apellido':forms.Textarea(attrs={'cols':40,'rows':1})
        }

class Cargagasto(forms.ModelForm):
    class Meta:
        model = Gastos
        fields =  ['cantidades','total_gasto','gasto','fechacarga']
        widgets = {
            'cantidades':forms.Textarea(attrs={'cols':3,'rows':1}),
            'total_gasto':forms.Textarea(attrs={'cols':8,'rows':1}),
            'fechacarga':DatePickerInput(options = {"disableMobile": "true"})
        }

class Formulario_del_gasto(forms.ModelForm):
    class Meta:
        model = Tiposdegastos
        fields = '__all__'

class Filtrargastos(forms.Form):
    seleccionar_gasto = forms.ModelChoiceField(
        queryset=Tiposdegastos.objects.all(),
        widget=autocomplete.ModelSelect2(attrs={'placeholder':'Nuevo gasto...'}))
