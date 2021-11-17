from django.db import models
from django.contrib.auth.models import User

# Create your models here.
## DASHBOARD IS FOR DONORS ##


class AddressTable(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="indirizzo")
    identificativo = models.CharField(max_length=400)
    via = models.CharField(max_length=400)
    cap = models.CharField(max_length=5)
    citta = models.CharField(max_length=400)
    provincia = models.CharField(max_length=2)
    note = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "indirizzo"
        verbose_name_plural = "indirizzi"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.identificativo


class FoodDonation(models.Model):
    """
    Il modello di una singola donazione di cibo
    """
    user_donor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="donazione"
    )
    listType = [
        (1, 'Cibo Cotto'),
        (2, 'Cibo Confezionato'),
        (3, 'Farmaci')
    ]
    listStatus = [
        ('D', 'Disponibile'),
        ('P', 'Prenotato'),
        ('C', 'Consegnato'),
        ('T', 'Temporaneamente non disponibile')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=listType)
    qty = models.IntegerField(default=1)  # qui forse dovremmo aggiungere 
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    status = models.TextField(max_length=1, choices=listStatus)
    indirizzo = models.ForeignKey(
        AddressTable, on_delete=models.CASCADE, related_name="indirizzo")

    class Meta:
        verbose_name = "Donazione Cibo"
        verbose_name_plural = "Donazioni Cibo"
        ordering = ['date_creation']

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.title


class Notification(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='sender_notification')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipient_notification')
    message = models.TextField()
    read = models.BooleanField(default=False)
    recieved_date = models.DateTimeField(auto_now_add=True)


