from django.shortcuts import render, redirect
from apps.chat_app.models import Room, Message
from django.http import HttpResponse, JsonResponse
from notifications.signals import notify
from apps.home.models import *
# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    #print('YEAH RIGUT')
    username = request.user
    room_details = Room.objects.get(name=room)
    
    return render(request, 'chat_app/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request,pk):
    #print('a')
  
    #print('AAAA')
    room = 'problema-'+ pk
    username = request.user
    #print('AAAA')
    if Room.objects.filter(name=room).exists():
        print(username)
        
        return redirect('/chat/'+room+'/?username='+str(username))
    else:
        new_room = Room.objects.create(name=room)
        new_room.ServiceRequest=  ServiceRequest.objects.filter(id=pk).first()
        new_room.save()
        
        orden = ServiceRequest.objects.filter(id=pk).first()
        customer = orden.customer
        #tecnico= username
        myurl = {"url": "iniciar_chat", "id":pk}
        myDescription ="Se ha creado una sala de chat para"+ orden.title
        notify.send(customer, recipient=customer, verb='message', description=myDescription, data=myurl )
        #return redirect('/'+room+'/?username='+str(username))
        return redirect('/chat/'+room+'/?username='+str(username))


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    
    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    
    room=Room.objects.filter(id=room_id).first()
    orden = ServiceRequest.objects.filter(id=room.ServiceRequest.id).first()
   
    customer= orden.customer
    tech=orden.takenby
    myurl = {"url": "iniciar_chat", "id":orden}
    
    print(username, customer,tech)
    
    if username == str(customer.username) :
        notify.send(tech, recipient=tech, verb='message', description='Tienes un mensaje Nuevo en '+room.name,data=myurl)
    elif username == str(tech.username) :
        notify.send(customer, recipient=customer, verb='message', description='Tienes un mensaje Nuevo en '+room.name,data=myurl)
        
    
    

    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    print("getting messages")
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

