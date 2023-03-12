# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
# 6th
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django import template
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404
from apps.chat_app.views import checkview
from django.template import RequestContext as ctx
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#app imports------------------------------------------------------->
from .models import *
from .forms import *
from taggit.models import *
import json
from notifications.signals import notify


from notifications.models import *

from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)






def select1(request):
    print('SELECT')
    data=[]
    try:
        action = request.POST['action']
        if action == 'search_computos':
            data = []
            for i in ComputoRegistrado.objects.filter(Area__id =1):
                print(i.modelo)
                data.append({'id':i.id,'modelo':i.modelo})
        else:
            data['error'] = 'Ha ocurrido un Error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def index(request):
    
    if request.user.is_superuser:
        listado_orders = ServiceRequest.objects.all().order_by('-status')
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,10)
            listado_orders = paginator.page(page)
        except:
            raise Http404
        
        context = {'segment': 'index','orders':listado_orders, 'paginator':paginator}
        searchQueryset= request.GET.get("search")
        if searchQueryset:
            print(searchQueryset)
        else:
            print('Nada Buscado')
        print('estas en el index')
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
    
    elif request.user.groups.filter(name='myUser'):
        print('USUARIO MIO AJAJAJA',request.user)
       # listado_orders = ServiceRequest.objects.filter(customer=request.user, status='Pending')[0:5]
        listado_orders = ServiceRequest.objects.filter((Q(customer=request.user) & Q(status='Pending') & Q(habilited=True) ) | (Q(customer=request.user) & Q(status='Taken by') & Q(habilited=True))   ).order_by('-date_created')[0:5] [::1]
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,5)
            listado_orders = paginator.page(page)
        except:
            raise Http404
        
        context = {'segment': 'index','orders':listado_orders, 'paginator':paginator}
        searchQueryset= request.GET.get("search")
        if searchQueryset:
            print(searchQueryset)
        else:
            print('Nada Buscado')
        print('estas en el index')
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
    else:
       # listado_orders = ServiceRequest.objects.filter((Q(customer=request.user) | Q(status='Pending')) )[0:10][::1]
   
        listado_orders = ServiceRequest.objects.filter((Q(customer=request.user) | Q(status='Pending')) )[::1]
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,5)
            listado_orders = paginator.page(page)
        except:
            raise Http404
        
        context = {'segment': 'index','orders':listado_orders, 'paginator':paginator}
        
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
    
    
    


@login_required(login_url="/login/")
def SearchResultsView(request):
    query = request.GET.get("q")
 


    listado_orders = ServiceRequest.objects.filter(
            Q(title__icontains=query))
   
    page= request.GET.get('page',1)
    try: 
        paginator = Paginator(listado_orders,2)
        listado_orders = paginator.page(page)
    except:
        raise Http404
        
    context = {'segment': 'index','orders':listado_orders, 'paginator':paginator}
    searchQueryset= request.GET.get("search")
    if searchQueryset:
        print(searchQueryset)
    else:
        print('Nada Buscado')
    print('estas en el index')
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
    
    
from django.views.generic.edit import (
    CreateView, UpdateView
)

from .forms import (
    ServiceRequestForm, EquipoFormSet, SoftwareFormSet
)
from .models import (
    Equipo,
    ServiceRequest,
    Software
)


class ProductInline():
    print('PRODUCT INLINE')
    form_class = ServiceRequestForm
    model = ServiceRequest
    template_name = "home/create.html"
   
    def form_valid(self, form):
        
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            
            return self.render_to_response(self.get_context_data(form=form))
        #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',self.request.user )
       
        self.object = form.save(commit=False)
        self.object.customer = self.request.user
        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        #return redirect('list_products')
        return redirect('home')

    def formset_variants_valid(self, formset):
        print('ESTE ES EL CUERPO DE TU REQUEST',self.request)
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        variants = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:
            variant.ServiceRequest = self.object
            variant.save()

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.ServiceRequest = self.object
            image.save()


class ProductCreate(ProductInline, CreateView):
    print('PRODUCT CREATE')
    def get_context_data(self, **kwargs):
        
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': EquipoFormSet(prefix='variants'),
                'images': SoftwareFormSet(prefix='images'),
            }
        else:
            return {
                'variants': EquipoFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
                'images': SoftwareFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }

    
class ProductUpdate(ProductInline, UpdateView):
    print('PRODUCT UPDATE')
    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'variants': EquipoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
            'images': SoftwareFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }


def delete_image(request, pk):
    try:
        image = Software.objects.get(id=pk)
    except Software.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('zupdate_product', pk=image.product.id)

    image.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('update_product', pk=image.product.id)


def delete_variant(request, pk):
    
    try:
        variant = Software.objects.get(id=pk)
    except Software.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('update_product', pk=variant.product.id)

    variant.delete()
    messages.success(
            request, 'Variant deleted successfully'
            )
    return redirect('update_product', pk=variant.product.id)


class ProductList(ListView):
    print('PRODUCT LIST')
    model = ServiceRequest
    template_name = "home/index.html"
    #context_object_name = "products"
   
    


@login_required(login_url="/login/")
def pages(request):

    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
def viewOrder(request,pk): 
    order = ServiceRequest.objects.get(id=pk)
    orderResponse =ServiceResponse.objects.filter(ServiceRequest = order.id).first()
    current_user = request.user
    customer = order.customer
    area= order.Area
    try:
        computo = ComputoRegistrado.objects.get(id=order.ComputoRegistrado.id)

    except:
      print('An exception occurred')
      computo = []
    #computo =get_object_or_404(ComputoRegistrado, id=order.ComputoRegistrado.id)
    
    print(area,computo)
    
    if current_user.groups.filter(name='myTech').exists():
        if (order.status == 'Solved'):
            print('revisando orden cerrada')
        else:
            order.takenby = request.user
            order.status = 'Taken by staff'
            order.save()
        
        myDescription="Tu orden" + str(order.title) + "ha sido tomada por" + str(request.user)
        
        myurl = {"url": "view_order", "id":pk}
        
        notify.send(customer, recipient=customer, verb='index', description=myDescription, data=myurl  )
    '''
    if order.takenby ==None:
        pass
    elif order.takenby != request.user or order.customer != customer:
        return redirect('home')
    
   
        
    '''
    form = ServiceResponseForm()
   
    
    equipos = Equipo.objects.filter(ServiceRequest=order)
    softwares = Software.objects.filter(ServiceRequest=order)
    
    context =  {
        'form':form,
        'order':order,
        'orderResponse':orderResponse,
        'equipos':equipos,
        'softwares':softwares,
        'computo':computo
       
        }
    
    if request.method == 'POST':
        print('recibimos tu formulario')
        form = ServiceResponseForm(request.POST,request.FILES)
 
       
     
        if form.is_valid():
            print('------------------------ISVALIDDD------------------------')

            myorder = form.save(commit=False)
            myorder.ServiceRequest = order
            print('------------------------ORDER------------------------')
            print(myorder)
            order.status='Solved'
            order.save()
            myorder.save()
            
            problema=ServiceRequest.objects.filter(id=pk).first()
            customer_info = problema.customer
            customer=User.objects.filter(id=customer_info.id).first()
            tech_info= problema.takenby
    
    
            tech=User.objects.filter(id=tech_info.id).first()
            Response =ServiceResponse.objects.filter(ServiceRequest=problema).first()
            Equipo_info= Equipo.objects.filter(ServiceRequest=problema)
    
    
    
    
    
    
            mycontext={
                'serviceRequest':problema,
                'customer':customer,
                'tech':tech,
                'response':Response,
                'equipo':Equipo_info
                }
            template_path='home/reporte.html'
            template=get_template(template_path)
            html = template.render(mycontext) 
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
           

    return render(request, 'home/orderView.html',context)          
                    
   
import pytz
from datetime import timedelta,datetime,date

@login_required(login_url="/login/")
def statistics(request):
    #----------------TAGS--------------------
    taglabels = []
    tagdata=[]
    #queryset = ServiceRequest.objects.order_by('date_created')[:5][::1]
    queryset = Tag.objects.all()
    #print(queryset)
    for tag in queryset:
       # print(order)
        taglabels.append(str(tag))
        tagdata.append(tag.taggit_taggeditem_items.count())
     
  
    
    
       # tagList= list(order.Tag.all())
       # for tag in tagList:
        
        #    taglabels.append(str(tag))
           
         #   counter=(ServiceRequest.objects.order_by('date_created').filter(tags=tag).count())
         #   tagdata.append(counter)
    
    #print('label',taglabels,'tada',tagdata)
            
            
    
     #----------------SEMANA-------------------
     
     
     
    datelabels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    datedata=[0,0,0,0,0,0,0]  
    today = datetime.today()
    idx = (today.weekday() + 1) % 7
    print(idx)
    lastSunday = today - timedelta(days=idx)
    print('EL ULTIMO DOMINGO FUE ',lastSunday)
    queryset1 = ServiceRequest.objects.order_by('date_created').filter(date_created__range = [lastSunday,today])
   # print(queryset1)
    for index, order in enumerate(queryset1):
        #print(order.date_created.strftime('%A') )
        if (order.date_created.strftime('%A') in datelabels):
            dayweekIndex=datelabels.index(order.date_created.strftime('%A'))
            print(dayweekIndex)
            index = datedata[dayweekIndex]
            print(index)
            #reemplazamos
            lastValue =   datedata[dayweekIndex] + 1
            datedata[dayweekIndex]= lastValue
            #lastValue= datedata[dayweekIndex] + 1
            #datedata.insert(dayweekIndex, lastValue)
            #print('se inserto el valor de', lastValue, 'en el indice',dayweekIndex, 'dia de la semana',datelabels.index(order.date_created.strftime('%A')) )
            #print(dayweekIndex)
            #print("se encuentra dentro de labels")
    print(datedata)
    #print('Domingo Fue',lastSunday)
    #week= today - timedelta(days=6)
        
    #print(datelabels)
    #print(datedata)
    #print('label',datelabels,'data',datedata)
    
    return render(request,'home/statistics.html',{
                'label':taglabels,
                'data':tagdata,
                'datelabel':datelabels,
               'datedate':datedata
            })
    

    
    
    
    
    return render(request, 'home/statistics.html')


@login_required(login_url="/login/")
def iniciarChat(request,pk):
   
    #print(pk)
    
    
    return (checkview(request,pk))

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

def generarReporte(request,pk):
    print('Generar Reporte')
    problema=ServiceRequest.objects.filter(id=pk).first()
    customer_info = problema.customer
    customer=User.objects.filter(id=customer_info.id).first()
    tech_info= problema.takenby
    
    
    tech=User.objects.filter(id=tech_info.id).first()
    Response =ServiceResponse.objects.filter(ServiceRequest=problema).first()
    Equipo_info= Equipo.objects.filter(ServiceRequest=problema)
    
    
    problema.status = "Solved"
    problema.save()
    
    
    context={
         'serviceRequest':problema,
         'customer':customer,
         'tech':tech,
         'response':Response,
         'equipo':Equipo_info
    }
    template_path='home/reporte.html'
    template=get_template(template_path)
    html = template.render(context) 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    #return FileResponse(,as_attachment=True,filename='reporte.pdf')
    

      





from django.forms import inlineformset_factory

def viewHardware(request):
    pass
    


def viewTables(request):
    user = request.user
    if request.user.groups.filter(name='myUser'):
        mySelectedOrders = ServiceRequest.objects.filter(Q(takenby=request.user) & Q(status='Taken by staff'))
        listado_orders = ServiceRequest.objects.filter(status='Solved')
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,2)
            listado_orders = paginator.page(page)
        except:
            raise Http404
        
        print(mySelectedOrders)
        context={
            'mySelectedOrders':mySelectedOrders,
            'listado_orders':listado_orders, 'paginator':paginator,
        
            
        }
        return render(request, 'home/tables.html',context)
       
    elif request.user.groups.filter(name='myTech'):
        mySelectedOrders = ServiceRequest.objects.filter(Q(takenby=request.user) & Q(status='Taken by staff'))
        listado_orders = ServiceRequest.objects.filter(status='Solved')
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,2)
            listado_orders = paginator.page(page)
        except:
            raise Http404
        
        print(mySelectedOrders)
        context={
            'mySelectedOrders':mySelectedOrders,
            'listado_orders':listado_orders, 'paginator':paginator,
        
            
        }
        return render(request, 'home/tables.html',context)
    elif    request.user.is_superuser:
        mySelectedOrders = ServiceRequest.objects.filter(Q(takenby=request.user) & Q(status='Taken by staff'))
        listado_orders = ServiceRequest.objects.all()
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,8)
            listado_orders = paginator.page(page)
        except:
            raise Http404
        
        print(mySelectedOrders)
        context={
            'mySelectedOrders':mySelectedOrders,
            'listado_orders':listado_orders, 'paginator':paginator,
        
            
        }
        return render(request, 'home/tables.html',context)
        

def SearchResultsViewTable(request):
    if request.user.groups.filter(name='myUser'):
        query = request.GET.get("q")

        listado_orders = ServiceRequest.objects.filter(
          (  ( Q(title__icontains=query) & Q(status__icontains='Solved')) &(Q(customer=request.user) )) |   (( Q(tags__name=query) & Q(status__icontains='Solved') )&(Q(customer=request.user) ) ))
    
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,2)
            listado_orders = paginator.page(page)
        except:
            raise Http404
            
        context = {'segment': 'index','listado_orders':listado_orders, 'paginator':paginator}
        searchQueryset= request.GET.get("search")
        if searchQueryset:
            print(searchQueryset)
        else:
            print('Nada Buscado')
        print('estas en el index')
        html_template = loader.get_template('home/tables.html')
        
    elif request.user.groups.filter(name='myTech'):
        query = request.GET.get("q")
        mySelectedOrders= ServiceRequest.objects.filter(Q(takenby=request.user) & Q(status='Taken by staff'))[::5]
        listado_orders = ServiceRequest.objects.filter(
          (( Q(title__icontains=query) & Q(status__icontains='Solved')) &(Q(customer=request.user) )) |  (( Q(tags__name=query) & Q(status__icontains='Solved') )&(Q(customer=request.user) ) ))
    
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,2)
            listado_orders = paginator.page(page)
        except:
            raise Http404
            
        context = {'segment': 'index','listado_orders':listado_orders, 'paginator':paginator,'mySelectedOrders':mySelectedOrders}
        searchQueryset= request.GET.get("search")
        if searchQueryset:
            print(searchQueryset)
        else:
            print('Nada Buscado')
        print('estas en el index')
        html_template = loader.get_template('home/tables.html')
    elif    request.user.is_superuser:
        query = request.GET.get("q")

        listado_orders = ServiceRequest.objects.filter(
            ( Q(title__icontains=query) & Q(status__icontains='Solved')) |   ( Q(tags__name=query) & Q(status__icontains='Solved') ) )
    
        page= request.GET.get('page',1)
        try: 
            paginator = Paginator(listado_orders,10)
            listado_orders = paginator.page(page)
        except:
            raise Http404
            
        context = {'segment': 'index','listado_orders':listado_orders, 'paginator':paginator}
        searchQueryset= request.GET.get("search")
        if searchQueryset:
            print(searchQueryset)
        else:
            print('Nada Buscado')
        print('estas en el index')
        html_template = loader.get_template('home/tables.html')
    return HttpResponse(html_template.render(context, request))
from django.http import JsonResponse




def getNotifications(request):
    print("-----------AAAAAAAAAAAAAAAAA-------")
    receptor=User.objects.get(pk=str(request.user.id))
    notifications=receptor.notifications.unread()
    context={'notifications':notifications}
    print(notifications)
    #thenotifications=receptor.Notification.unread()
    #print(thenotifications)
    html_template = loader.get_template('includes/navigation.html')
  #  return HttpResponse(html_template.render(context, request))
    return render(request,'includes/noti.html',{'notifications':notifications})
   # return JsonResponse()
   
   
   
def notifcations(request):
    print("-----------AAAAAAAAAAAAAAAAA-------")
    receptor=User.objects.get(pk=str(request.user.id))
    notifications=receptor.notifications.unread()
 
    messajes=receptor.notifications.filter(Q(target_object_id=receptor) and Q(verb='message'))[:1]
    print(messajes)
    myMessajes = messajes
    #context={'notifications':notifications}
    print(notifications)
    #thenotifications=receptor.Notification.unread()
    #print(thenotifications)

  #  return HttpResponse(html_template.render(context, request))
    return render(request,'home/notifications.html',{'notifications':notifications,'MS':myMessajes})
   # return JsonResponse()

def readNotifications(request,pk):
    print('_____________DELETE NOTIFICATION___________')
    receptor=User.objects.get(pk=str(request.user.id))
    print('PK',pk)
    notificationToDelete=receptor.notifications.filter(id=pk)
    notificationToDelete.mark_all_as_read()
    
    print(notificationToDelete)
    print(pk)
    notifications=receptor.notifications.unread()
    print("la notificacion ha sido leida")
    return render(request,'includes/notilist.html',{'notifications':notifications,'messajes':notifications})


def eliminateOrder(request,pk):
    order=ServiceRequest.objects.filter(id=pk)
    
    order.update(habilited=False)
    return redirect('home')


           
                    
                    
def create_area(request):
    
    
    form = AreaForm()

    context =  {
        'form':form,
    
        }
    
    print('--------------------post--------------------')
    print(request.POST)
    
    if request.method == 'POST':

        print('------------------form------------------')
        #print(form)
        print('------------------cformset------------------')
        #print(cformset)
        #print(request.user)
  
        #print('FORM ERROR',form.errors)
       # print('FORMSET ERROR',cformset.errors)
        form = AreaForm(request.POST,request.FILES)
  
       
        print(form)
        if form.is_valid():

            order = form.save(commit=False)
     
            order.save()
             
    return render(request, 'home/create_area.html', context)

def create_equipo(request):
    
    form = ComputoRegistradoForm()

    context =  {
        'form':form,
    
        }
    
    print('--------------------post--------------------')
    print(request.POST)
    
    if request.method == 'POST':
        

        print('------------------form------------------')
        #print(form)
        print('------------------cformset------------------')
 
        form = ComputoRegistradoForm(request.POST,request.FILES)
  
       
        print(form)
        if form.is_valid():
           

            order = form.save(commit=False)
            order.user=request.user
     
            order.save()
             
    

                    

    return render(request,'home/create_equipo.html', context)
