from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import enrich_with_user_details, restrict_to_traders


@login_required
@enrich_with_user_details
@restrict_to_traders
def traders_index(request, *args, **kwargs):
    context = kwargs['context']
    context['current_url_name'] = 'traders-index'
    return render(request, 'traders/index.html', context)


@login_required
@enrich_with_user_details
@restrict_to_traders
def traders_mb(request, *args, **kwargs):
    context = kwargs['context']
    context['current_url_name'] = 'traders-mb'
    return render(request, 'traders/mass_balance.html', context)


@login_required
@enrich_with_user_details
@restrict_to_traders
def traders_histo(request, *args, **kwargs):
    context = kwargs['context']
    context['current_url_name'] = 'traders-histo'
    return render(request, 'traders/archives.html', context)


@login_required
@enrich_with_user_details
@restrict_to_traders
def import_doc(request, *args, **kwargs):
    context = kwargs['context']
    return render(request, 'traders/import_doc.html', context)


@login_required
@enrich_with_user_details
@restrict_to_traders
def import_mb_doc(request, *args, **kwargs):
    context = kwargs['context']
    return render(request, 'traders/import_mb_doc.html', context)
