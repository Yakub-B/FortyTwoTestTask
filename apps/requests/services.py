from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render

from apps.requests.models import RequestModel


def last_ten_requests_not_ajax(request):
    try:
        latest_request_id = RequestModel.objects.all().latest().id
    except ObjectDoesNotExist:
        raise Http404

    if request.GET.get('priority'):
        priority = request.GET.get('priority')
        qs = RequestModel.objects.filter(priority=priority)[:10]
    else:
        qs = RequestModel.objects.all()[:10]

    context = {'requests': qs, 'latest_request_id': latest_request_id}
    return render(request, 'requests.html', context)


def last_ten_requests_ajax(request):
    # in get parameter 'id' we get id of the last request displayed
    # on page
    if request.GET.get('id'):
        # looking for newer requests
        # (with id grater then id we got from ajax)
        new_qs = RequestModel.objects.filter(
            id__gt=request.GET['id']).order_by('priority', 'timestamp')[:10]
        if new_qs.exists():
            # serializing queryset
            data = list(new_qs.values())
            counter = 0
            for obj in data:
                try:
                    obj['user'] = new_qs[counter].user.username
                    counter += 1
                except AttributeError:
                    counter += 1
            latest_request_id = data[-1]['id']
            data = {
                'requests': data, 'latest_request_id': latest_request_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'data': None})
    raise Http404
