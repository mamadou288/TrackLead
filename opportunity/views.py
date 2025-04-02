from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from prospects.models import Prospect
from .forms import OpportunityForm
from .models import Opportunity

@login_required
def add_opportunity(request, prospect_id):
    prospect = get_object_or_404(Prospect, pk=prospect_id, owner=request.user)

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.prospect = prospect
            opportunity.save()
            return redirect('prospect-detail', pk=prospect.pk)
    else:
        form = OpportunityForm()

    return render(request, 'opportunity/opportunity_form.html', {
        'form': form,
        'prospect': prospect
    })

@login_required
def create_opportunity(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            # Get the prospect from the form data
            prospect_id = request.POST.get('prospect')
            if prospect_id:
                prospect = get_object_or_404(Prospect, pk=prospect_id, owner=request.user)
                opportunity = form.save(commit=False)
                opportunity.prospect = prospect
                opportunity.save()
                return redirect('opportunity-detail', pk=opportunity.pk)
    else:
        form = OpportunityForm()
    
    # Get all prospects for the dropdown
    prospects = Prospect.objects.filter(owner=request.user)
    
    return render(request, 'opportunity/opportunity_form.html', {
        'form': form,
        'prospects': prospects,
        'create': True
    })

@login_required
def opportunity_list(request):
    # Filter opportunities through the prospect's owner
    opportunities = Opportunity.objects.filter(prospect__owner=request.user)
    
    # Calculate statistics
    total_amount = opportunities.aggregate(total=Sum('montant_estime'))['total'] or 0
    in_progress_count = opportunities.filter(statut='in_progress').count()
    won_count = opportunities.filter(statut='won').count()
    
    context = {
        'opportunities': opportunities,
        'total_amount': total_amount,
        'in_progress_count': in_progress_count,
        'won_count': won_count,
    }
    return render(request, 'opportunity/opportunity_list.html', context)

@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, prospect__owner=request.user)
    return render(request, 'opportunity/opportunity_detail.html', {'opportunity': opportunity})

@login_required
def opportunity_update(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, prospect__owner=request.user)

    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect('opportunity-detail', pk=opportunity.pk)
    else:
        form = OpportunityForm(instance=opportunity)

    return render(request, 'opportunity/opportunity_form.html', {
        'form': form,
        'edit': True,
    })

@login_required
def opportunity_delete(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, prospect__owner=request.user)
    opportunity.delete()
    return redirect('opportunity-list')
