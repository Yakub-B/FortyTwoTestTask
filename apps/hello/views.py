from django.views.generic import TemplateView

from apps.hello.models import ProfileModel


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = ProfileModel.objects.first()
        return context
