from django.db import models
from django.conf import settings

SOURCE_CHOICES = [
    ('call', 'Appel téléphonique'),
    ('email', 'Email'),
    ('event', 'Événement / Salon'),
    ('referral', 'Recommandation'),
    ('web', 'Formulaire web'),
    ('social', 'Réseaux sociaux'),
    ('other', 'Autre'),
]

class Prospect(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Lié à un utilisateur (le commercial qui gère ce prospect)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company}"
