from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Prospect
from .forms import ProspectForm

@login_required
def prospect_list(request):
    prospects = Prospect.objects.filter(owner=request.user)
    return render(request, 'prospects/prospect_list.html', {'prospects': prospects})

@login_required
def prospect_create(request):
    if request.method == 'POST':
        form = ProspectForm(request.POST)
        if form.is_valid():
            prospect = form.save(commit=False)
            prospect.owner = request.user  # lie au commercial connecté
            prospect.save()
            return redirect('prospect-list')
    else:
        form = ProspectForm()

    return render(request, 'prospects/prospect_form.html', {'form': form})

@login_required
def prospect_detail(request, pk):
    prospect = get_object_or_404(Prospect, pk=pk, owner=request.user)
    return render(request, 'prospects/prospect_detail.html', {'prospect': prospect})

@login_required
def prospect_update(request, pk):
    prospect = get_object_or_404(Prospect, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProspectForm(request.POST, instance=prospect)
        if form.is_valid():
            form.save()
            return redirect('prospect-detail', pk=prospect.pk)
    else:
        form = ProspectForm(instance=prospect)

    return render(request, 'prospects/prospect_form.html', {'form': form, 'update': True})

@login_required
def prospect_delete(request, pk):
    prospect = get_object_or_404(Prospect, pk=pk, owner=request.user)
    prospect.delete()
    return redirect('prospect-list')