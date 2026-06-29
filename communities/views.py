from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import DonationForm, NeedForm
from .models import Community, Donation, Need


@login_required
def community_list(request):
    communities = Community.objects.filter(is_active=True)
    search = request.GET.get('q', '').strip()
    province = request.GET.get('provincia', '')

    if search:
        communities = communities.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    if province:
        communities = communities.filter(province=province)

    return render(request, 'communities/list.html', {
        'communities': communities,
        'search': search,
        'province': province,
        'provinces': Community.Province.choices,
    })


@login_required
def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk, is_active=True)
    category = request.GET.get('categoria', '')
    needs = community.needs.filter(status=Need.Status.ACTIVE)
    if category:
        needs = needs.filter(category=category)

    return render(request, 'communities/detail.html', {
        'community': community,
        'needs': needs,
        'category': category,
        'categories': Need.Category.choices,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def donate(request, need_pk):
    need = get_object_or_404(Need, pk=need_pk, status=Need.Status.ACTIVE)
    form = DonationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > need.remaining_amount:
            form.add_error('amount', f'El monto no puede superar ${need.remaining_amount:,.0f}.')
        else:
            donation = Donation.objects.create(
                need=need,
                donor=request.user,
                amount=amount,
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'amount': float(donation.amount),
                    'community': need.community.name,
                    'need': need.title,
                    'confirmation_code': donation.confirmation_code,
                })
            messages.success(request, f'¡Donación exitosa! Código: {donation.confirmation_code}')
            return redirect('communities:detail', pk=need.community.pk)

    return render(request, 'communities/partials/donation_modal.html', {
        'need': need,
        'form': form,
    })


@login_required
@require_POST
def donate_api(request, need_pk):
    need = get_object_or_404(Need, pk=need_pk, status=Need.Status.ACTIVE)
    try:
        amount = Decimal(request.POST.get('amount', '0'))
    except InvalidOperation:
        return JsonResponse({'success': False, 'error': 'Monto inválido.'}, status=400)

    if amount <= 0:
        return JsonResponse({'success': False, 'error': 'El monto debe ser mayor a 0.'}, status=400)
    if amount > need.remaining_amount:
        return JsonResponse({
            'success': False,
            'error': f'El monto no puede superar ${need.remaining_amount:,.0f}.',
        }, status=400)

    donation = Donation.objects.create(
        need=need,
        donor=request.user,
        amount=amount,
    )
    return JsonResponse({
        'success': True,
        'amount': float(donation.amount),
        'community': need.community.name,
        'need': need.title,
        'confirmation_code': donation.confirmation_code,
    })


@login_required
def my_needs(request):
    if not request.user.is_community:
        messages.error(request, 'Solo usuarios de tipo Comunidad pueden gestionar necesidades.')
        return redirect('communities:list')

    community = getattr(request.user, 'community_profile', None)
    form = NeedForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if not community:
            messages.error(request, 'Tu cuenta no tiene una comunidad asociada. Contactá al administrador.')
        else:
            need = form.save(commit=False)
            need.community = community
            need.save()
            messages.success(request, 'Necesidad agregada exitosamente')
            return redirect('communities:my_needs')

    active_needs = []
    if community:
        active_needs = community.needs.filter(status=Need.Status.ACTIVE)

    return render(request, 'communities/my_needs.html', {
        'form': form,
        'community': community,
        'active_needs': active_needs,
    })
