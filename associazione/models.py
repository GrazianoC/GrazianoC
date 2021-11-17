from django.db import models
from django.contrib.auth.models import User
from donatore.models import FoodDonation, AddressTable

# Create your models here.
## DASHBOARD ASS is for the RECEIVER ##


class OrdTemp(models.Model):
    """
    Il modello di un ordine. Ogni Ordine è composto da più donazioni
    """
    user_assoc = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ordinetemporaneo"
    )
    id_donazione = models.ForeignKey(
        FoodDonation, on_delete=models.CASCADE, related_name="id_donazione"
    )
    donatore = models.IntegerField(default=0)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ordine Temporaneo"
        verbose_name_plural = "Ordini Temporanei"
        ordering = ['date_creation']

class Ordini(models.Model):
    """
    Il modello di un ordine da legare al dettaglio
    """

    # Decidere come creare l'indice dell'ordine
    user_assoc = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_assoc"
    )
    num_ordine = models.TextField(default="")
    donatore = models.IntegerField(default=0)

    date_confimation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ordine"
        verbose_name_plural = "Ordini"
        ordering = ['date_confimation']

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.num_ordine


class Dettaglio_Ordini(models.Model):
    id_ordine = models.ForeignKey(
        Ordini, on_delete=models.CASCADE, related_name="ordini")
    id_donazione = models.ForeignKey(
        FoodDonation, on_delete=models.CASCADE, related_name="donazioni")

class DonorReceipt(models.Model):
## RICEVUTA DEL DONATORE UTILE PER RENDICONTARE LA DONAZIONE ##

    # data del documento #
    date = models.DateField()

    '''
    # estremi del donatore #
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="estremi_cedente")
    
    # estremi del ricevente #
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="estremi_cessionario")
    '''  
    
    # nome e cognome del vettore #
    carrier = models.TextField(max_length=200)

    # destinazione #
    destination = models.ForeignKey(AddressTable, on_delete=models.CASCADE, related_name="indirizzo_destinazione")

    # quantità e qualità donazione #
    donation = models.ForeignKey(Ordini, on_delete=models.CASCADE, related_name="dati_donazione")

    class Meta:
        verbose_name = "Documento di Trasporto"
        verbose_name_plural = "Documenti di Trasporto"


    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})