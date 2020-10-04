from django.utils.deprecation import MiddlewareMixin

from apps.requests.models import RequestModel


class RequestLoggerMiddleware(MiddlewareMixin):
    """
    Middleware that saves all HTTPRequests into db
    using RequestModel
    """
    def process_request(self, request):
        """
        Getting data from request and creating RequestModel instance
        """
        if not request.is_ajax():
            request_instance = RequestModel()
            request_instance.url = request.build_absolute_uri(request.get_full_path())
            request_instance.method = request.method
            request_instance.encoding = request.encoding
            request_instance.content_type = request.content_type
            if request.user.is_authenticated:
                request_instance.user = request.user

            request_instance.save()
