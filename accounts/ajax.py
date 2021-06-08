from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View, UpdateView
from django.apps import apps
from django.urls import resolve
import json

class AjaxContextData:
    def get_context_dat(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.kwargs
        [filter.pop(key, None) for key in ['pk', 'id', 'uuid','slug']]
        # context['object_list'] = self.get_queryset().filter(**filter)
        context['%s_list' % self.model.__name__.lower(
        )] - self.get_queryset().filter(**filter)
        return context

class AjaxValidForm:
    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data['form_id'] = form.instance._meta.model_name
            data['html_list'] = render_to_string(
                self.ajax_list, context, self.request)
            data['message'] = 'Save Successful.'
        else:
            data['form_is_valid'] = False
            data['message'] = 'Form validation error!'
        data['html_form'] = render_to_string(
            self.ajax_modal, context, request=self.request)
        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return super().form_valid(form)

class AjaxUpdateView(AjaxContextData, AjaxValidForm, UpdateView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_modal, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)