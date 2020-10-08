from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from apps.requests.models import RequestModel


def last_ten_requests_not_ajax(request):
    try:
        latest_request_id = RequestModel.objects.all().latest().id
    except ObjectDoesNotExist:
        raise Http404

    sort_by = request.GET.get('sort_by')
    if sort_by:
        if 'priority' in sort_by:
            qs = RequestModel.objects.select_related('url_priority').order_by(sort_by, '-timestamp')[:10]
        else:
            qs = RequestModel.objects.select_related('url_priority').order_by(sort_by, '-timestamp')[:10]
    else:
        qs = RequestModel.objects.select_related('url_priority').order_by(
            '-url_priority__priority', '-timestamp')[:10]

    context = {'requests': qs, 'latest_request_id': latest_request_id}
    return render(request, 'requests.html', context)


def last_ten_requests_ajax(request):
    # in get parameter 'id' we get id of the last request displayed
    # on page
    if request.GET.get('id'):
        # looking for newer requests
        sort_by = '-url_priority__priority'
        if request.GET.get('sort_by'):
            sort_by = request.GET.get('sort_by')
        new_qs = RequestModel.objects.select_related('url_priority').all().order_by(
            sort_by, '-timestamp')[:10]
        new_requests_count = RequestModel.objects.filter(id__gt=request.GET['id']).count()

        # serializing queryset
        data = list(new_qs.values())
        counter = 0
        for obj in data:
            obj['priority'] = new_qs[counter].url_priority.priority
            obj['url'] = new_qs[counter].url_priority.path
            obj['timestamp'] = timezone.localtime(new_qs[counter].timestamp).strftime('%b. %e, %Y, %l:%M %P.')
            try:
                obj['user'] = new_qs[counter].user.username
                counter += 1
            except AttributeError:
                counter += 1
        data.reverse()
        latest_request_id = RequestModel.objects.all().latest().id
        data = {
            'requests': data, 'latest_request_id': latest_request_id,
            'new_requests_count': new_requests_count
        }
        return JsonResponse(data)

    raise Http404
