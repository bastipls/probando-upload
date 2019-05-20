from django import forms
from .models import Alumno,Evento

class AlumnoForm (forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rut_alumno'].widget.attrs.update({'required':'True','oninput':'checkRut(this)'})
  


    class Meta:
        model = Alumno
        fields = ('rut_alumno',)
class EventoForm (forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_evento'].widget.attrs.update({'required':'True'})
        self.fields['fecha_evento'].widget.attrs.update({'placeholder':'dd/MM/YYY'})

    fecha_evento = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))   
    class Meta:
        model = Evento
        fields = ('nombre_evento','estado_evento','fecha_evento',)