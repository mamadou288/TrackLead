from django.db import models
from django.conf import settings
from prospects.models import Prospect

class Opportunity(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('in_progress', 'En cours'),
        ('won', 'Gagné'),
        ('lost', 'Perdu'),
    ]

    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='opportunities')
    name = models.CharField(max_length=255)
    montant_estime = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    date_cloture = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_statut_display()} ({self.montant_estime} €)"
