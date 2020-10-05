from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from apps.requests.models import RequestModel


class LastTenRequestsView(View):
    """
       This view will render page with last 10 requests
       and process ajax requests to get newer requests from db
       """

    def get(self, request):
        """
        Main method that process get requests, both ajax and common
        """
        if not request.is_ajax():
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
        else:
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
                    latest_request_id = data[-1]['id']
                    data = {
                        'requests': data, 'latest_request_id': latest_request_id
                    }
                    return JsonResponse(data)
                else:
                    return JsonResponse({'data': None})
            raise Http404
