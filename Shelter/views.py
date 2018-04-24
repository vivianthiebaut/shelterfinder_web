from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from .models import Shelter
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("/home")
    return render(request, "Shelter/index.html", {})

def user_login(request):
    if request.user.is_authenticated:
        return redirect("/home")
    username = request.POST['username']
    password = request.POST['pass']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/home")
    else:
        return render(request, "Shelter/index.html", {"error":"Invalid Login"})


def user_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'Shelter/register.html', {'form': form})

@login_required
def home(request):
    gender = request.GET.get('gender')
    shelter_type = request.GET.get('shelter_type')
    name = request.GET.get('name')
    shelters = Shelter.objects.all()
    if name is not None:
        shelters = shelters.filter(name__icontains=name)
    if gender is not None:
        shelters = shelters.filter(restrictions__icontains=gender)
    if shelter_type is not None:
        shelters = shelters.filter(restrictions__icontains=shelter_type)

    return render(request, 'Shelter/home.html', {'shelters':shelters})

@login_required
def shelter_details(request, id):
    shelter = Shelter.objects.get(id = id)
    message = ""
    if (request.method == 'POST'):
        num_beds = request.POST.get("bed_qtd")
        if num_beds is not None:
            action = request.POST.get("request_type")
            print(action)
            if action == "cancel":
                if shelter.cancel_reservation(int(num_beds), request.user):
                    message = "Successful cancellation"
                else:
                    message = "Unsuccessful cancellation"
            elif action == "reserve":
                if shelter.make_reservation(int(num_beds), request.user):
                    message = "Successful reservation"
                else:
                    message = "Unsuccessful reservation"
    return render(request, 'Shelter/details.html', {'shelter':shelter, 'message':message})