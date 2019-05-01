from django.db import models
from django.utils import timezone
from mysite import settings
# Create your models here.
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key = True)
    rut_alumno = models.CharField(max_length = 10)
    nombre_alumno = models.CharField(max_length=80, blank=True,null=True)
    carrera_alumno = models.CharField(max_length=80, blank=True,null=True)
    evento_asistio_alumno = models.CharField(max_length = 40, blank=True,null=True)
    fecha_evento_asistio_alumno = models.DateField(default=timezone.now,null=True)

    def __str__(self):
        return self.rut_alumno 


class Evento (models.Model):
    estado = ( 
        ('Activo','Activo'),
        ('Cerrado','Cerrado')
    )
    id_evento = models.AutoField(primary_key = True)
    nombre_evento = models.CharField(max_length = 40)
    estado_evento = models.CharField(max_length = 20,choices=estado,null=True,default='Activo')
    fecha_evento  = models.DateField(default=timezone.now,null=True)

    def __str__(self):
        return self.nombre_evento
class Alumno_duoc(models.Model):
    id_alumno_duoc = models.IntegerField(blank=True,primary_key=True)
    rut_alumno_duoc = models.CharField(max_length=15,blank=True,null=True)
    nombre_alumno_duoc = models.CharField(max_length=80, blank=True,null=True)
    carrera_alumno_duoc = models.CharField(max_length=80, blank=True,null=True)
    def __str__(self):
        return self.nombre_alumno_duoc
     