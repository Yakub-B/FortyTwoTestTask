from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View

from apps.hello.forms import EditProfileDataForm
from apps.hello.models import ProfileModel


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = ProfileModel.objects.first()
        return context


class EditProfileDataView(LoginRequiredMixin, View):
    def get(self, request):
        profile_instance = ProfileModel.objects.first()
        form = EditProfileDataForm(instance=profile_instance)
        context = {'form': form, 'profile': profile_instance}
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        profile_instance = ProfileModel.objects.first()
        form = EditProfileDataForm(request.POST, instance=profile_instance)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
                return redirect('hello:index')
            return JsonResponse({'success': True})
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
