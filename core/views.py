from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from prospects.models import Prospect
from opportunity.models import Opportunity
from django.utils import timezone
from datetime import timedelta

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    # Get prospects count
    nb_prospects = Prospect.objects.filter(owner=request.user).count()
    
    # Get opportunities statistics
    opportunities = Opportunity.objects.filter(prospect__owner=request.user)
    nb_opportunities = opportunities.count()
    nb_won = opportunities.filter(statut='won').count()
    nb_lost = opportunities.filter(statut='lost').count()
    
    # Calculate total revenue from won opportunities
    total_revenue = opportunities.filter(statut='won').aggregate(
        total=Sum('montant_estime')
    )['total'] or 0
    
    # Calculate conversion rate
    taux_conversion = round((nb_won / nb_opportunities * 100) if nb_opportunities > 0 else 0, 1)
    
    # Get recent prospects (last 5)
    recent_prospects = Prospect.objects.filter(
        owner=request.user
    ).order_by('-created_at')[:5]
    
    # Get recent opportunities (last 5)
    recent_opportunities = Opportunity.objects.filter(
        prospect__owner=request.user
    ).order_by('-created_at')[:5]
    
    # Calculate monthly revenue for the last 6 months
    monthly_revenue = []
    for i in range(5, -1, -1):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        revenue = opportunities.filter(
            statut='won',
            created_at__range=(month_start, month_end)
        ).aggregate(
            total=Sum('montant_estime')
        )['total'] or 0
        monthly_revenue.append(revenue)
    
    context = {
        'nb_prospects': nb_prospects,
        'nb_opportunities': nb_opportunities,
        'nb_won': nb_won,
        'nb_lost': nb_lost,
        'total_revenue': total_revenue,
        'taux_conversion': taux_conversion,
        'recent_prospects': recent_prospects,
        'recent_opportunities': recent_opportunities,
        'monthly_revenue': monthly_revenue,
    }
    
    return render(request, 'core/dashboard.html', context)