from flatpickr import DatePickerInput
from django import forms
from .models import Pedidos,Tiposdegastos,Gastos
from datetime import datetime,date
from dal import autocomplete

class FormularioNuevoPedido(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields =  ['fecha','nombre_cliente','comentario']
        widgets = {
            'fecha': DatePickerInput(),
            'comentario':forms.Textarea(attrs={'rows':5}
            )
        }

class Fecha(forms.Form):
    dia= forms.DateField(widget=DatePickerInput())
    # options={"dateFormat":""}


class Filtrargastos(forms.Form):
    seleccionar_gasto = forms.ModelChoiceField(
        queryset=Tiposdegastos.objects.all(),
        widget=autocomplete.ModelSelect2(attrs={'placeholder':'Nuevo gasto...'}))

class Cargagasto(forms.ModelForm):
    class Meta:
        model = Gastos
        fields =  ['cantidades','total_gasto','gasto','fechacarga']
        widgets = {
            'cantidades':forms.Textarea(attrs={'cols':3,'rows':1}),
            'total_gasto':forms.Textarea(attrs={'cols':8,'rows':1}),
            'fechacarga':DatePickerInput()
        }

class Formulario_del_gasto(forms.ModelForm):
    class Meta:
        model = Tiposdegastos
        fields = '__all__'
