from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
        
        else:
            messages.success(request, "There was an error logging in.")

        return redirect('home')
    
    else:
        records = Record.objects.all()
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")

    return redirect('home')



def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)

        return render(request, 'record.html', {'record': record})
    
    else:
        messages.success(request, "You must be logged in to view that page!")
        
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        record.delete()
        messages.success(request, "Record deleted successfully.")
    
    else:
        messages.success(request, "You must be logged in to delete that record!")

    return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:

        if request.method == 'POST':

            if form.is_valid():
                record = form.save()
                #Authenticate and login
                messages.success(request, "Record added.")
                
                return redirect('home')
            
        else:
            return render(request, 'add_record.html', {'form': form})
        
    else:
        messages.success(request, "You must be logged in.")
                
        return redirect('home')
    

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance = record)

        if request.method == "POST":
            if form.is_valid():
                record = form.save()
                messages.success(request, "Record has been updated.")
                return redirect('home')
        
        return render(request, "update_record.html", {'form': form})

    else:
            messages.success(request, "You must be logged in.")

            return redirect('home')