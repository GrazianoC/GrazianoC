
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView  
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from donatore.models import FoodDonation, AddressTable, Notification
from .models import Dettaglio_Ordini, OrdTemp, Ordini
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def Dashboard(request):
    context =  {'gruppo': request.session['gruppo'], 'carrello': OrdTemp.objects.filter(user_assoc=request.user).count()}  
        
    if (request.session['gruppo']=='Associazione'):
      return render(request, 'associazione/dashboard.html', context)
    else:
      return render(request, 'associazione/404.html', context)

# Create your views here.
class FoodDistListView(LoginRequiredMixin, ListView):
    model = FoodDonation
    def get_queryset(self):
        #return FoodDonation.objects.filter(status="D") #ritorna solo i disponibili
        return FoodDonation.objects.all()
    template_name = 'associazione/food_list_as.html'
    context_object_name = 'food_list'
    paginate_by = 10
    def get_context_data(self, **kwargs):  #Serve per inserire un extra context nella pagina
     context = super().get_context_data(**kwargs)
     context['carrello'] = OrdTemp.objects.filter(user_assoc=self.request.user).count() #conta quanti oggetti ci sono nel carrello
     context['gruppo'] =  self.request.session['gruppo']
     context['lista_carrello']= OrdTemp.objects.filter(user_assoc=self.request.user) #Lista  oggetti del carrello
     print("Lista_carrello:")
     print (context)
     return context
   
@login_required    
def TemporaryOrder(request, pk):
    #INSERIRE SVUOTAMENTO CARRELLO DOPO X 
    # bisogna cntrollare se l'id della donazione non è già stato prenotato da altra associazione
    # qui va il controllo se non esiste già lo stesso id nel carrello
    #esiste_temp=get_object_or_404(OrdTemp, id=pk)
  
    try:
     esiste_temp=OrdTemp.objects.get(id=pk) 
     if esiste_temp:
        print ("Già inserito!!!!")
        request.session['errore'] = "Donazione già presente nel carrello"
        messages.warning(request, 'Donazione già presente nel carrello.')
        return redirect('foodlistas' )
    except OrdTemp.DoesNotExist:
      esiste_temp= None
    donazione=FoodDonation.objects.get(id=pk)
    o = OrdTemp.objects.create(id_donazione=donazione, user_assoc=request.user, donatore=donazione.user_donor_id)
    o.save()
    FoodDonation.objects.filter(id=pk).update(status='T')  #Aggiorno lo stato della donazione in Temporanemanete non disponibile
    messages.success(request, 'Donazione inserita nel carrello.')
    return redirect('foodlistas' )

    
class CartListView(LoginRequiredMixin, ListView):
    
    def get_queryset(self):
        a1= OrdTemp.objects.filter(user_assoc=self.request.user)
        #a1 = FoodDonation.objects.prefetch_related('id')
        a2 = a1.select_related('id_donazione')
        #a1 = OrdTemp.objects.select_related('id_donazione')
        
        print ((a2.query)) 
        #print (self.request.user)
        print ((a2.values()))  #visualizza i dati all.interno della 
        return a2
    template_name = 'associazione/carrello.html'
    context_object_name = 'cart_list'
    def get_context_data(self, **kwargs):  #Serve per inserire un extra context nella pagina
     context = super().get_context_data(**kwargs)
     context['carrello'] = OrdTemp.objects.filter(user_assoc=self.request.user).count() #conta quanti oggetti ci sono nel carrello
     context['gruppo'] =  self.request.session['gruppo']
     context['lista_carrello']= OrdTemp.objects.filter(user_assoc=self.request.user) #Lista  oggetti del carrello
     return context
    
@login_required   
def CartDeleteItem (request, pk):
  try:
     esiste_temp=OrdTemp.objects.get(id=pk)
     
     if esiste_temp:
        a=FoodDonation.objects.filter(id=esiste_temp.id_donazione.id) 
        print (pk)
        print (FoodDonation.objects.filter(id=esiste_temp.id_donazione.id))
        a.update(status='D')
        esiste_temp.delete()
        print ("Esiste in fase di eliminazione!!!")
        messages.success(request, 'Donazione eliminata dal carrello.')
        return redirect('carrello' )
  except OrdTemp.DoesNotExist:
      esiste_temp= None
  return redirect('carrello' )
  
@login_required   
def InviaOrdine (request):      
   var_ultimo_ordine=-1
   oggetti_carrello=OrdTemp.objects.filter(user_assoc=request.user) #prendo tutti gli oggetti inseriti nel carrello
   donatori_carrello=OrdTemp.objects.all().filter(user_assoc=request.user).values('donatore').distinct()
   #se non leggo con la donazione non posso estrapolarmi il donatore 
   a2 = oggetti_carrello.select_related('id_donazione') #join su fooddonation
   ListaVuota = [] #lista vuota per inserire prodotti del carrello
   #donatori=a2.objects.raw('Select user_donor_id from donatore_fooddonation group by user_donor_id')
  
   for donatori in donatori_carrello: #faccio un ciclo sulle donazioni 
    print ("-----------------")
    print ('Donatore dal carrello') 
    print (donatori['donatore']) #estraggo l'id del donatore dal dizionario
    
   
    try:
       ultimo_ordine=Ordini.objects.order_by('-num_ordine')[0] #Cerco ultimo numero_ordine (se la tabela è vuota darebbe errore)
    except Ordini.DoesNotExist:
       var_ultimo_ordine=0    
    if var_ultimo_ordine==0: 
         var_ultimo_ordine=var_ultimo_ordine+1
    else:
         var_ultimo_ordine=int(ultimo_ordine.num_ordine)+1 
    print ('*************')        # verifiche
    #print  (type(ultimo_ordine)) # verifiche
    print('Ultimo ordine estratto dal database')
    print  ((ultimo_ordine.num_ordine)) # verifiche
    print ('--->Ordine da inserire<---')
    print (var_ultimo_ordine) 
    
    # print (donatori[donatore]) controllo che mi genera errore
    o = Ordini.objects.create(user_assoc=request.user, num_ordine=var_ultimo_ordine,  donatore=donatori['donatore']) #inserisco i dati nella tabella ordini
    o.save()  #li salvo
    print ('Ho inserito l'' ordine')
    for oggetto in a2: #controllo ogni oggetto della lista delle donazioni
      
      if donatori['donatore']==oggetto.id_donazione.user_donor_id:
            
            #Inserire qui il dettaglio ordini
       #print ('Id donatore da ordini temporanei ')
       #print( oggetto.id_donazione.user_donor_id) #controllo
       rif_ordine=Ordini.objects.get(num_ordine=var_ultimo_ordine)
       rif_donazione=FoodDonation.objects.get(id=oggetto.id_donazione.id)
       print ('riferimento ordine')
       print (rif_ordine)
       p=Dettaglio_Ordini.objects.create(id_ordine=rif_ordine, id_donazione=rif_donazione) #Inserisco il dettaglio ordine
       p.save()
       ListaVuota.append(oggetto.id_donazione_id) #inserisco l'id della donazione nella lista
       
      print ("-----------------") 
      notifica=Notification.objects.create(sender=request.user, recipient=User.objects.get(id=oggetto.id_donazione.user_donor_id), message= "Hai ricevuto un nuovo ordine" ) #Inserisco una notifica di ordine
      notifica.save() #la salvo
   aggiorna_stato_donazioni=FoodDonation.objects.filter(id__in=ListaVuota) #prendo tutti i valori della lista (quindi tutti i dati del carrello)
   
   aggiorna_stato_donazioni.update(status='P') #aggiorno lo stato delle donazioni come prenotata
   oggetti_carrello.delete() # svuoto il carrello
   context= {"carrello": OrdTemp.objects.filter(user_assoc=request.user).count()} #azzero il carrello
   context['gruppo'] =  request.session['gruppo']
   context['lista_carrello']= OrdTemp.objects.filter(user_assoc=request.user) #Lista  oggetti del carrello
   #creare ordine
   #inserire il dettaglio dell'ordine
   

   messages.success(request, 'Ordine creato con successo.') # invio una notifica al browser
   return render(request, "associazione/ordine_confermato.html", context)

  