from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from stats.models import Statistics


@login_required
@transaction.atomic
def statistics(request):
    stat = Statistics.objects.get(hospital=request.user.person.hospital_id)
    admitted = stat.number_admitted_patients()
    num_visits = stat.avg_num_visits_patient()
    avg_length = stat.avg_visits_length()
    prescriptions = stat.get_popular_prescriptions()
    reason = stat.get_most_common_reason()
    return render(request, 'stats/stats.html', {
        'admitted': admitted,
        'avg_length': avg_length,
        'num_visits': num_visits,
        'prescriptions': prescriptions,
        'reason': reason,
    })


