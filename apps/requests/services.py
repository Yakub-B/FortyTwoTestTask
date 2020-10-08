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

    sort_by = request.GET.get('sort_by', '-url_priority__priority')
    qs = RequestModel.objects.select_related('url_priority').order_by(sort_by, '-timestamp')[:10]

    context = {'requests': qs, 'latest_request_id': latest_request_id}
    return render(request, 'requests.html', context)


def serialize_requests(requests_queryset):
    data = []
    for obj in requests_queryset:
        serialized_request = {
            'id': obj.id,
            'priority': obj.url_priority.priority,
            'url': obj.url_priority.path,
            'timestamp': timezone.localtime(obj.timestamp).strftime('%b. %e, %Y, %l:%M %P.'),
            'encoding': obj.encoding,
            'method': obj.method,
            'content_type': obj.content_type,
        }
        try:
            serialized_request['user'] = obj.user.username
        except AttributeError:
            serialized_request['user'] = None
        data.append(serialized_request)

    data.reverse()
    return data


def last_ten_requests_ajax(request):
    # in get parameter 'id' we get id of the last request displayed on page
    if request.GET.get('id'):
        # looking for newer requests
        sort_by = request.GET.get('sort_by', '-url_priority__priority')
        new_qs = RequestModel.objects.select_related('url_priority').all().order_by(
            sort_by, '-timestamp')[:10]
        new_requests_count = RequestModel.objects.filter(id__gt=request.GET['id']).count()
        # serializing queryset
        data = serialize_requests(new_qs)
        latest_request_id = RequestModel.objects.latest().id
        data = {
            'requests': data, 'latest_request_id': latest_request_id,
            'new_requests_count': new_requests_count
        }
        return JsonResponse(data)

    raise Http404
