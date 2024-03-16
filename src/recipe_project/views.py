from django.shortcuts import render, redirect        
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

def login_view(request):
    error_message = None 
    form = AuthenticationForm()

    if request.method == 'POST':                        
        form =AuthenticationForm(data=request.POST)
    
        if form.is_valid():                                
            username=form.cleaned_data.get('username')      
            password = form.cleaned_data.get('password')    

            user=authenticate(username=username, password=password)
            if user is not None:                    
                login(request, user)                
                return redirect('recipes:records-search') 
        else:
            error_message = "Invalid username or password"
    context ={                                             
       'form': form,                                 
       'error_message': error_message                     
            }
    return render(request, 'auth/login.html', context)  

def logout_view(request):                                  
   logout(request)             
   return render(request, 'auth/success.html') 

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')