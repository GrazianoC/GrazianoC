from django.shortcuts import render
from django.views.generic.list import ListView  
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import FoodDonation, AddressTable
from associazione.models import Ordini   
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
# Create your views here.


class FoodListView(LoginRequiredMixin, ListView):
    model = FoodDonation
    def get_queryset(self):
        return FoodDonation.objects.filter(user_donor=self.request.user)
    template_name = 'donatore/food_list.html'
    context_object_name = 'food_list'
    paginate_by = 10
    def get_context_data(self, **kwargs):  #Serve per inserire un extra context nella pagina
     context = super().get_context_data(**kwargs)
     if (self.request.session['gruppo'] != 'Donatore'):   #Questo controllo server per restringere la visualizzazione di questa pgina solo ai donatori
         return render(request, 'donatore/404.html', context)
         
     context['gruppo'] =  self.request.session['gruppo'] 
     print (context)
     return context
   
    
       
    
def FoodWhat(request):
    context =  {'gruppo': request.session['gruppo']} 
    return render(request, 'donatore/whatfoot.html', context)
   
def Dashboard(request):
    context =  {'gruppo': request.session['gruppo']}     
    if (request.session['gruppo']=='Donatore'):
      return render(request, 'donatore/dashboard.html', context)
    else:
      return render(request, 'donatore/404.html', context)
#class Dashboard(LoginRequiredMixin, ListView):
#    model = Ordini
#    def get_queryset(self, request):
#        #return Ordini.objects.filter(user_donor=self.request.user)
#        queryset = super(Ordini, self).get_queryset(request)
#        sql = "SELECT * FROM Ordini inner join dettaglio_ordini on ordini.num_ordine=dettaglio_ordine.id_ordine_id"
#        queryset = Ordini.objects.raw(sql)
#        return queryset
    
    
#    template_name = 'donatore/dashboard.html'
#    context_object_name = 'food_list'
#    paginate_by = 10
#    def get_context_data(self, **kwargs):  #Serve per inserire un extra context nella pagina
#     context = super().get_context_data(**kwargs)
#     if (self.request.session['gruppo'] != 'Donatore'):   #Questo controllo server per restringere la visualizzazione di questa pgina solo ai donatori
#         return render(request, 'donatore/404.html', context)
         
#     context['gruppo'] =  self.request.session['gruppo'] 
#     print (context)
#     return context





class FoodDetail(LoginRequiredMixin, DetailView):
    model = FoodDonation
    template_name = 'donatore/detailfood.html'
    

class FoodInsert(LoginRequiredMixin, CreateView): #se inserisci LoginRequiredMixin non puoi inserire il form se non sei già connesso
    login_url = '/accounts/'
    model = FoodDonation
    fields = ['title', 'description', 'type', 'qty', 'indirizzo'] #'__all__' inserisce tutti i campi del modello 
    
    success_url = reverse_lazy('foodlist')
    template_name='donatore/newfood.html'
    def get_form(self, *args, **kwargs):
        form = super(FoodInsert, self).get_form(*args, **kwargs)
     
        form.fields['indirizzo'].queryset = AddressTable.objects.filter(user_id=self.request.user)
        return form

    def form_valid(self, form):
        print (self.request.user)
        form.instance.user_donor = self.request.user          #in assnza dei campi a video assegno al campo user_honor il nome dell'utente connesso
        form.instance.status="D"  
       
                                    #in assnza dei campi a video assegno al campo status inl valore D
        return super(FoodInsert, self).form_valid(form)

class FoodEdit(LoginRequiredMixin, UpdateView): 
    login_url = '/accounts/'
    model = FoodDonation
    fields = ['title', 'description', 'type', 'qty', 'indirizzo'] #'__all__' inserisce tutti i campi del modello 
    
    success_url = reverse_lazy('foodlist')
    template_name='donatore/editfood.html'
    def get_form(self, *args, **kwargs):
        form = super(FoodEdit, self).get_form(*args, **kwargs)
     
        form.fields['indirizzo'].queryset = AddressTable.objects.filter(user_id=self.request.user)
        return form
    def form_valid(self, form):
        print (self.request.user)
        form.instance.user_donor = self.request.user          #in assnza dei campi a video assegno al campo user_honor il nome dell'utente connesso
        form.instance.date_modification=datetime.now()        #la data modifica si aggiorna solo in update
        form.instance.status="D"                              #in assnza dei campi a video assegno al campo status inl valore D
        return super(FoodEdit, self).form_valid(form)

class FoodDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/'
    model = FoodDonation
    success_url = reverse_lazy('foodlist')
    
    

class AddressListView(LoginRequiredMixin, ListView):
    model = AddressTable
    def get_queryset(self):
        return AddressTable.objects.filter(user_id=self.request.user)
    template_name = 'donatore/addresses_list.html'
    context_object_name = 'addresses_list'
   
class AddressInsert(LoginRequiredMixin, CreateView): #se inserisci LoginRequiredMixin non puoi inserire il form se non sei già connesso
    login_url = '/accounts/'
    model = AddressTable
    fields = ['identificativo', 'via', 'citta', 'cap', 'provincia', 'note'] #'__all__' inserisce tutti i campi del modello 
    
    success_url = reverse_lazy('address')
    template_name='donatore/new_address.html'

    def form_valid(self, form):
        print (self.request.user)
        form.instance.user_id = self.request.user          #in assnza dei campi a video assegno al campo user_honor il nome dell'utente connesso
        
        return super(AddressInsert, self).form_valid(form)        
    
    
class OrderListView(LoginRequiredMixin, ListView):
    model = Ordini
    template_name = 'donatore/order_list.html'
    context_object_name = 'order_list'
    paginate_by = 10
    
    