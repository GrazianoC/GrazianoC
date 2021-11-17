#from accounts.models import FoodUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Permission, Group
from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView  

# Create your views here.
#non utilizzo la classe loginview perchè devo fare in modo che il sistema reindirrizzi 'utente alla dashbord in base al valore del gruppo
#class CustomLoginView(LoginView):
#    template_name = 'accounts/login.html'
#    fields = '__all__'
#    redirect_authenticated_user = True

#    def get_success_url(self):
        
#        return reverse_lazy('foodlist')

def Login_User(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
       
        username =  request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #print(username,password,user)
        if user is None:
            messages.success(request, 'Username or Password is incorrect')
            return HttpResponseRedirect('/accounts/login/')
        else:
           login(request, user)
           group = None
           
           
           if request.user.groups.exists():
             group = request.user.groups.all()[0].name
             print ("Group = "+ group)
             request.session['gruppo']= group
             print (request.session['gruppo'])
             if group == 'Donatore':
               return HttpResponseRedirect("/donatore/foodlist/")
             if group == 'Associazione':
               return HttpResponseRedirect("/associazione/foodlistas/")
           else:
                return HttpResponseRedirect("/admin/")
          # else:
           #return HttpResponseRedirect("/donatore/foodlist")
           #return HttpResponse('You are not authorised to access this page')

        
        
                   
        #return HttpResponseRedirect("/donatore/foodlist")
    else:  
        form = AuthenticationForm()
    context = {"form": form}  
    return render(request, "accounts/login.html", context)

#La view registration fatta in questa maniera non ha senso 
#class UserRegistration(LoginView): 
#    template_name = 'accounts/registration.html'
#    model = FoodUser
#    redirect_authenticated_user = True
#    success_url = reverse_lazy('foodlist')


   # def form_valid(self, form):
        #suser = form.save()
    #    if user is not None:
    #        login(self.request, user)
     #   return super(UserRegistration, self).form_valid(form)

    #def get(self, *args, **kwargs):
     #   if self.request.user.is_authenticated: 
     #       return redirect('foodlist')
     #   return super(UserRegistration, self).form_valid(form)

#il form userregistration include solo 3 campi username, password e password confirmation. Bisogna estendere il form estendendo la classe userregistration in forms.py
def UserRegistration(request): #definsico una view per creare l'utenza
    if request.method == "POST":  #per la registrazione è ammesso solamente il metodo POST
        form = SignUpForm(request.POST) #inizializzo l'oggetto form con tutto il postback del form
        if form.is_valid(): #se il form risulta valido allora proseguo con l'assegnazione delle variabili per la creazione utente
            username =  form.cleaned_data["username"] #varibile username
            first_name = form.cleaned_data["first_name"] #variabile first_name
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            groups=form.cleaned_data["groups"] #variabile gruppo restituisce l'id del gruppo (2 - donatori, 1 -associazione)
            print (username, first_name, email, password, groups )
            User.objects.create_user(username=username, first_name=first_name,  password=password, email=email) #Creo l'utente nella tabella users memorizzando le 4 variabili rispettivamente nei 4 campi
            
            my_group = Group.objects.get(pk=groups) #cerco nella tabella groups l'id del gruppo associazione o donatore e lo memorizzo nella variabile my_group
            user1 = User.objects.get(username = username) #in user1 memorizzo l'id del nome utente appena creato memorizzato nella variabile username
            my_group.user_set.add(user1) #associo al gruppo selezionato l'utente appena creato.
            #User.groups.add(name=groups)
           
            user = authenticate(username=username, password=password) # effettuo l'accesso- 
            login(request, user) #Effettuo la login
            group = None
            
           
            if request.user.groups.exists():
             group = request.user.groups.all()[0].name
             print ("Group = "+ group)
             if group == 'Donatore':
               return HttpResponseRedirect("/donatore/foodlist/")
             if group == 'Associazione':
               print ("/associazione/foodlistas/")
               return HttpResponseRedirect("/associazione/foodlistas/")
            else:
                return HttpResponseRedirect("/admin/")
            return HttpResponseRedirect("/donatore/foodlist/")
    else:
        form = SignUpForm()
    context = {"form": form}
    return render(request, "accounts/registration.html", context)



 
class ProfileListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profilo'
    # Bisogna inserire le informazioni relative al gruppo dell'utente 