from django.utils.deprecation import MiddlewareMixin

from apps.requests.models import RequestModel, UrlPriority

PATHS_TO_IGNORE = ('static', 'media', 'favicon.ico')


class RequestLoggerMiddleware(MiddlewareMixin):
    """
    Middleware that saves all HTTPRequests into db
    using RequestModel
    """
    @staticmethod
    def check_request(request):
        """
        This function checks if the request should be logged to the database
        """
        if request.is_ajax():
            return False
        for path in PATHS_TO_IGNORE:
            if path in request.path:
                return False
        return True

    def process_request(self, request):
        """
        Getting data from request and creating RequestModel instance
        """
        if self.check_request(request):
            request_url = request.build_absolute_uri(request.get_full_path())
            url_priority_instance, _ = UrlPriority.objects.get_or_create(path=request_url)
            request_instance = RequestModel()
            request_instance.method = request.method
            request_instance.encoding = request.encoding
            request_instance.content_type = request.content_type
            request_instance.url_priority = url_priority_instance
            if request.user.is_authenticated:
                request_instance.user = request.user

            request_instance.save()
