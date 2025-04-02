from django import forms
from .models import Opportunity

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'montant_estime', 'statut', 'date_cloture', 'notes']
