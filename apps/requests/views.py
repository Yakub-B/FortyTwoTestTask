from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic.base import View

from apps.requests.forms import RequestPriorityForm
from apps.requests.models import RequestModel
from apps.requests.services import last_ten_requests_not_ajax, last_ten_requests_ajax


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
            return last_ten_requests_not_ajax(request)
        else:
            return last_ten_requests_ajax(request)


class EditRequestPriorityView(View):
    def post(self, request):
        request_instance = RequestModel.objects.get(id=request.POST.get('id'))
        form = RequestPriorityForm(request.POST, instance=request_instance)
        if form.is_valid():
            url = request_instance.url
            requests_to_update = RequestModel.objects.filter(url=url)
            requests_to_update.update(priority=form.cleaned_data.get('priority'))
            form.save()
            return redirect('requests:last_requests')
        else:
            return HttpResponseBadRequest()
