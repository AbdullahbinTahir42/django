from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room,Topic,Message
from django.db.models import Q, Count
from .forms import RoomForm,TopicForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    page = 'login_page'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('home')  
        else:
            
            messages.error(request, "Invalid username or password.")
    context = {'page' : page}
    return render(request, 'base/login_register.html', context) 


def logoutuser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Unable to register!!")
    return render(request,'base/login_register.html',{'form': form})


def home(request):
    q = request.GET.get('q', '') 
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
    )
    room_count = rooms.count()  
  
    topics = Topic.objects.annotate(room_count=Count('room'))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        return redirect('room', pk=room.id)


    context = {'room' : room, 'room_messages' : room_messages , 'participants' :participants}        
    return render(request, 'base/room.html',context)

@login_required(login_url='login_page')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request,'base/room_form.html',context)



def AddTopic(request):
    form = TopicForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request,'base/topic_form.html',context)


def UpdateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You Are not Allowed Here")

    if request.method == 'POST':
        form = RoomForm(request.POST,instance= room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form} 
    return render(request,'base/room_form.html',context)   


def UpdateTopic(request,pk):
    topic = Topic.objects.get(id=pk)
    form = TopicForm(instance=topic)
    if request.method == 'POST':
        form = TopicForm(request.POST,instance= topic)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form} 
    return render(request,'base/topic_form.html',context)  

@login_required(login_url='login_page')
def delete(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("You Are not Allowed Here")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})