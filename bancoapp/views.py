from django.shortcuts import render, redirect
from django.views.generic import *
from .models import *
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


# Create your views here.


class index(ListView):
    model = Usuarios
    template_name = "index.html"
    context_object_name = "usuarios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        prestamos = Prestamo.objects.all()

        valorCuotasPagadas = 0

        #Cuotas que ya se han pagado
        for prestamo in prestamos:
            
            prestamoInteres = prestamo.prestamo

            if prestamo.prestamista.socio == True:
                prestamoInteres = (prestamo.prestamo * 0.01) + prestamoInteres
            else:
                prestamoInteres = (prestamo.prestamo * 0.025) + prestamoInteres

            prestamoInteres = (prestamoInteres / prestamo.cuotasPrestamo)

            cuotaPagada = prestamo.cuotasPorPagar * prestamoInteres
            valorCuotasPagadas += cuotaPagada

        context['ganaciaActual'] = valorCuotasPagadas

        proyeccionGanacia = 0

        #Cuotas que se debería pagar
        for prestamo in prestamos:
            
            prestamoInteres = prestamo.prestamo

            if prestamo.prestamista.socio == True:
                prestamoInteres = (prestamo.prestamo * 0.01) + prestamoInteres
            else:
                prestamoInteres = (prestamo.prestamo * 0.025) + prestamoInteres

            prestamoInteres = (prestamoInteres / prestamo.cuotasPrestamo)

            cuotasFaltantes = prestamo.cuotasPrestamo - prestamo.cuotasPorPagar

            cuotaPagada = cuotasFaltantes * prestamoInteres
            
            proyeccionGanacia += cuotaPagada

        context['proyeccionGanacia'] = proyeccionGanacia

        return context 



class registro(CreateView):
    model = Usuarios
    fields = ["username","last_name","password","cedula","socio"]
    template_name = 'registroUsuario.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            nombre = request.POST['username']
            apellido = request.POST['last_name']
            password = request.POST['password']
            cedula = request.POST['cedula']
            try:
                socio = request.POST['socio']
            except:
                socio="False"
            

        if socio == "on":
            socio = "True"
        else:
            socio="False"

        try:
            user = Usuarios.objects.create(username=nombre , last_name=apellido, password=password, cedula=cedula, socio=socio)
            user.save()
            login(request, user)

            if user.is_superuser:
                return redirect('index')
            else:
                return redirect('informacion-usuario', user.id)
        
        except IntegrityError:
            return render(request, 'registroUsuario.html', {
                'message': 'Hubo un problema, intente otra vez'
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn'] = 'Registro'
        context['redireccion'] = 'login'
        return context 

class actualizar(UpdateView):
    model = Usuarios
    fields = ["username","last_name","password","cedula","socio"]
    template_name = 'registroUsuario.html'
    
    def post(self, request, *args, **kwargs):
        user = Usuarios.objects.get(id=self.kwargs['pk'])
        if request.method == 'POST':
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            password = request.POST['password']
            cedula = request.POST['cedula']
            socio = request.POST['socio']
        
        if socio == "on":
            socio = "True"
        else:
            socio="False"

        try:
            user.nombre =nombre
            user.apellido=apellido 
            user.password=password 
            user.cedula=cedula 
            user.socio=socio

            user.save()
            return redirect('index')
        
        except IntegrityError:
            return render(request, 'registroUsuario.html', {
                'message': 'Hubo un problema, intente otra vez'
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn'] = 'Actualizar'
        context['redireccion'] = 'index'

        return context

class eliminar(DeleteView):
    model = Usuarios
    template_name = 'confirmDelete.html'
    context_object_name = 'usuario'
    
    def get_success_url(self):
        return reverse("index")

class InvertirFondo(CreateView):
    model= Fondo
    fields=["ahorro"]
    template_name='fondo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inversionista'] = Usuarios.objects.get(id=self.kwargs['pk'])
        context['btn'] = 'Invertir'
        return context

    def post(self, request, *args, **kwargs):
        inversionista= Usuarios.objects.get(id=self.kwargs['pk'])

        if request.method == "POST":
            ahorro=request.POST['ahorro']

            try:
                instancia = FondoBanco.objects.get(id=6)
                instancia.total += int(ahorro)
                instancia.save()
            except:
                instancia = FondoBanco.objects.create(total = int(ahorro))
                instancia.save()
                

            try:
                instancia = Fondo.objects.get(inversionista = inversionista)
                instancia.ahorro += int(ahorro)
                instancia.save()

                return redirect('informacion-usuario', inversionista.id)

            except:
                instancia = Fondo.objects.create(inversionista = inversionista, ahorro = ahorro)
                instancia.save()
                return redirect('informacion-usuario', inversionista.id)
            
        


def DarPrestamo(request, id):
    
    prestamista = Usuarios.objects.get(id=id)

    if request.method == 'POST':
        prestamo = int(request.POST['prestamo'])
        cuotas = request.POST['cuotas']

        if prestamista.socio == True:
            inversion = Fondo.objects.get(inversionista = prestamista)
            if int(prestamo) > inversion.ahorro * 0.90:
                return render(request, 'prestamo.html', {
                    'message': 'El monton no debe superar el 90% del total ahorrado por el inversor',
                    'prestamista': prestamista
                })
            else:
                
                fondoTotal = FondoBanco.objects.get(id=6)
            
                if prestamo < fondoTotal.total:    
                    instacia = Prestamo.objects.create(prestamista = prestamista, prestamo = prestamo, cuotasPrestamo = cuotas)
                    instacia.save()
                    
                    fondoTotal.total -= prestamo
                    fondoTotal.save()

                    return redirect('index')
                else:
                    return render(request, 'prestamo.html', {
                    'message': 'el prestamo es mayor que el fondo total del banco. ',
                    'prestamista': prestamista
                })
        else:

            fondoTotal = FondoBanco.objects.get(id=6)
            
            if prestamo < fondoTotal.total:    
                instacia = Prestamo.objects.create(prestamista = prestamista, prestamo = prestamo, cuotasPrestamo = cuotas)
                instacia.save()

                fondoTotal.total -= prestamo
                fondoTotal.save()

                return redirect('index')
            else:
                return render(request, 'prestamo.html', {
                'message': 'el prestamo es mayor que el fondo total del banco. ',
                'prestamista': prestamista
            })

    else:
        return render(request, 'prestamo.html', {'prestamista': prestamista, 'fondoTotal': FondoBanco.objects.get(id=6)})


def informacion(request, id):

    if request.method == "GET":

        usuario = Usuarios.objects.get(id=id)

        try:
            inversion = Fondo.objects.get(inversionista = usuario.id)
        except:
            inversion = False

        try:
            prestamo = Prestamo.objects.get(prestamista = usuario.id)

            prestamoInteres = prestamo.prestamo

            if usuario.socio == True:
                prestamoInteres = (prestamo.prestamo * 0.01) + prestamoInteres
            else:
                prestamoInteres = (prestamo.prestamo * 0.025) + prestamoInteres

            prestamoInteres = (prestamoInteres / prestamo.cuotasPrestamo)


        except:
            prestamoInteres = 0
            prestamo = False


        context = {
            'user': usuario,
            'prestamoInteres': prestamoInteres,
            'prestamo': prestamo,
            'inversion': inversion,
        }

        return render(request, 'informacion.html', context)
    else:
        usuario = Usuarios.objects.get(id=id)
        prestamo = Prestamo.objects.get(prestamista = usuario.id)
        cuotaPagada = request.POST['cuotas']
        prestamo.cuotasPorPagar += int(cuotaPagada)
        prestamo.save()
        return redirect('informacion-usuario', usuario.id)

        

def login_view(request):
    
    if request.user.is_active:
        return redirect('index')

    if request.method == 'POST':
        nombre = request.POST['username']
        password = request.POST['password']

        try:

            user = authenticate(username = nombre, password= password)
            
            if user is None:
                user = Usuarios.objects.get(username = nombre, password = password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('index')
                else:
                    return redirect('informacion-usuario', user.id)
        except:
            return render(request, 'credenciales/login.html', {
                'message': 'Invalid user and / or password'
            })
            
    else:
        return render(request, 'credenciales/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



    