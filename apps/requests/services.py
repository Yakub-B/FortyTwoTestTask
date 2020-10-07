from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render

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
            qs = RequestModel.objects.select_related('url_priority').order_by(sort_by)[:10]
    else:
        qs = RequestModel.objects.select_related('url_priority').all()[:10]

    context = {'requests': qs, 'latest_request_id': latest_request_id}
    return render(request, 'requests.html', context)


def last_ten_requests_ajax(request):
    # in get parameter 'id' we get id of the last request displayed
    # on page
    if request.GET.get('id'):
        # looking for newer requests
        # (with id grater then id we got from ajax)
        new_qs = RequestModel.objects.select_related('url_priority').filter(
            id__gt=request.GET['id']).order_by('url_priority__priority', 'timestamp')[:10]
        if new_qs.exists():
            # serializing queryset
            data = list(new_qs.values())
            print(data)
            counter = 0
            for obj in data:
                try:
                    obj['user'] = new_qs[counter].user.username
                    obj['priority'] = new_qs[counter].url_priority.priority
                    obj['url'] = new_qs[counter].url_priority.url
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
