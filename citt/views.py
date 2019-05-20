from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import Alumno,Evento,Alumno_duoc
from .forms import AlumnoForm,EventoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from .resources import AlumnoResource
from django.utils import timezone
from django.contrib import messages
import os
from django.http import HttpResponse, Http404
eventoAsisteGlobal = "Seleccione evento"

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['txtuser'].lower()
        password = request.POST['txtpass']
        user = authenticate(request,username = username, password=password)
        if user:
            login(request,user)
            
            return HttpResponseRedirect(reverse('registro'))
        else:
            messages.error(request,'Credenciales incorrectas')

            return render(request, 'citt/login.html',context)
    else:
        return render(request,'citt/login.html',context)  

@login_required(login_url='login')
def logout_view(request):
  
    if request.method == 'POST':
        logout(request)
    return redirect('login')
@login_required(login_url='login')
def registro_view(request):
    global eventoAsisteGlobal 
    eventos = Evento.objects.filter(estado_evento='Activo')
    date = timezone.now
    if request.method == 'POST':
        rutAlumno = request.POST.get('txtrut',True).upper()
        #httpsÑ--portal.sidiv.registrocivil.cl-docstatus_RUN¿20057170'3/type¿CEDULA/serial¿108608430/mrz¿108608430298112232111223
       

        #Todo este metodo del rut es solo para scanners en ingles
        if rutAlumno[0].lower() == 'H':
            elrut = rutAlumno.split('¿')[1].replace('/type','').replace("'","-")
            if elrut.find('-') == 7:
                 nuevoRut = elrut[:-1]
            else:
                nuevoRut = elrut
        else:
           nuevoRut = rutAlumno.replace("'","-")
        
        
        duoc_exists = Alumno_duoc.objects.filter(rut_alumno_duoc=nuevoRut).exists()
        if duoc_exists == True:
            nombreAlumno = Alumno_duoc.objects.values_list('nombre_alumno_duoc',flat=True).filter(rut_alumno_duoc=nuevoRut).first()
            carreraAlumno = Alumno_duoc.objects.values_list('carrera_alumno_duoc',flat=True).filter(rut_alumno_duoc=nuevoRut).first()
        else:
            nombreAlumno = "Alumno nuevo"
            carreraAlumno = "Alumno nuevo"
        eventoAsiste = request.POST.get('txteventoasiste',True)
        fechaAsiste = request.POST.get('txtfechaasiste',True)
        eventoThere = Evento.objects.filter(nombre_evento=eventoAsiste).filter(estado_evento='Activo').exists()
        alu = Alumno.objects.filter(rut_alumno=nuevoRut).filter(evento_asistio_alumno=eventoAsiste).filter(fecha_evento_asistio_alumno=fechaAsiste).exists()
        
        if alu == False:
            if eventoThere == True:    
                atributos = Alumno(rut_alumno =nuevoRut,nombre_alumno=nombreAlumno,carrera_alumno=carreraAlumno,evento_asistio_alumno = eventoAsiste,fecha_evento_asistio_alumno=fechaAsiste) 
                eventoAsisteGlobal = eventoAsiste
                atributos.save()
                messages.success(request,nombreAlumno)
            else:
                eventoAsisteGlobal = 'Seleccione evento'
                return redirect('error_evento')
        else:
            return redirect('error')
    
    context = {'eventos':eventos,
                'eventoAsisteGlobal':eventoAsisteGlobal,
                'date':date}            
    return render(request,'citt/registro.html',context)



@user_passes_test(lambda u:u.is_superuser, login_url=('login'))
def crear_evento_view(request):
    global eventoAsisteGlobal
    if request.method == 'POST':
        nombreEvento = request.POST.get('txtevent',True)
        eventoAsisteGlobal = nombreEvento
        atributos = Evento(nombre_evento = nombreEvento)
        atributos.save()
        messages.success(request,nombreEvento)
    todos_eventos = Evento.objects.all()
    query = request.GET.get('q') 
    
    if query:
        todos_eventos = todos_eventos.filter(
                                            Q(nombre_evento__icontains=query)       
                                           )
    context = {'todos_eventos':todos_eventos}  
    return render(request, 'citt/evento.html',context)


@login_required(login_url='login')  
def error_view(request):
    context = {}
    return render(request,'citt/error.html',context) 

@login_required(login_url='login')
def error_evento_view(request):
    context = {}
    return render(request,'citt/error_evento.html',context) 
 
@login_required(login_url='login')
def listar_view(request):
    todos_ruts = Alumno.objects.all()
    todos_eventos = Evento.objects.all()
    query_rut = request.GET.get('q_rut')
    query_evento = request.GET.get('q_evento')
    evento = ''
    if query_rut and query_evento:
        todos_ruts = todos_ruts.filter(
                                        Q(rut_alumno=query_rut ) &
                                        Q(evento_asistio_alumno= query_evento)
                                        )
        asiste = todos_ruts.count()
        evento= query_evento
        if asiste == 0:
            evento = ''
            messages.error(request, "No se encontro nada :'(")
    elif query_rut or query_evento :
        
        todos_ruts = todos_ruts.filter(
                                        Q(rut_alumno=query_rut ) |
                                        Q(evento_asistio_alumno= query_evento)
                                        )
        asiste = todos_ruts.count()
        evento= query_evento
        if asiste == 0:
            evento = ''
            messages.error(request, "No se encontro nada :'(")
    else:
        todos_ruts = Alumno.objects.all()
        asiste =  todos_ruts.count()
        evento = ''
    

    context = {'todos_ruts':todos_ruts,
                'asiste':asiste,
                'todos_eventos':todos_eventos,
                'evento':evento}
    return render(request,'citt/listar.html',context)
@user_passes_test(lambda u:u.is_superuser, login_url=('login'))
def modificar_view(request,pk):
    alumno = get_object_or_404(Alumno,pk=pk)
  
    if request.method == 'POST':
        form = AlumnoForm(request.POST,instance=alumno)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.save()
            return redirect('listar')
    else:
        form = AlumnoForm(instance = alumno)
    context = {'form':form,
                'alumno':alumno }
    return render(request,'citt/modificar.html',context)

@user_passes_test(lambda u:u.is_superuser, login_url=('login'))
def modificar_evento_view(request,pk):
    evento = get_object_or_404(Evento,pk=pk)
    if request.method == 'POST':
       form = EventoForm(request.POST,instance=evento) 
       if form.is_valid():
           evento = form.save(commit=False)
           evento.save()
           return redirect('crear_evento')
    else:
        form = EventoForm(instance = evento)
    context = {'form':form,
                'evento':evento }
    return render(request,'citt/modificar_evento.html',context)

@user_passes_test(lambda u:u.is_superuser, login_url=('login'))
def eliminar_evento_view(request,pk):
    evento = get_object_or_404(Evento,pk=pk)
    evento.delete()
    return redirect('crear_evento')

@user_passes_test(lambda u:u.is_superuser, login_url=('login'))
def eliminar_view(request,pk):
    alumno = get_object_or_404(Alumno,pk=pk)
    alumno.delete()

    return redirect('listar')

@user_passes_test(lambda u:u.is_superuser, login_url=('login'))
def export_csv(request):
    alumno_resource = AlumnoResource()
    dataset = alumno_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alumnos.xls"'
    
    return response

@login_required(login_url='login')
def descargar_manual(request):
    if request.user.is_superuser:
        file_path=os.path.join('media','manuales','Manual_Admin.docx' )
    elif request.user.is_staff:
        file_path=os.path.join('media','manuales', 'Manual_Ayudante.docx' )
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
 



        
