from django.shortcuts import render,redirect
from userauths.form import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from userauths.models import User


# Create your views here.


def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, You account was created successfully.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()


    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)



def login_view(request):  
    
    if request.method == "POST":
        email = request.POST.get("email") #user enter email 
        password = request.POST.get("password") #user entered password Us

        try:
            user = User.objects.get(email=email,is_superuser=False)
            user = authenticate(request, email = email, password =password)


            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user} you logged in")
                return redirect("core:index" )
            
            else:
                messages.warning(request,  "user does not exist, Create an account")
            
        except:
            messages.warning(request, f"User with  {email} does not exist")


    return render(request,"userauths/log-in.html" )
def logout_view(request):
    messages.success(request,"you loged out !")
    logout(request)
    # Clear the session
    request.session.flush()
    return render(request,"userauths/log-in.html")
      