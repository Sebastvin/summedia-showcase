from django.shortcuts import render
from django.views import View

from .forms import TextInputForm


class BaseTextView(View):
    form_class = TextInputForm
    template_name = ""
    extra_context = {}
    title = ""

    def get_context_data(self, **kwargs):
        context = {
            "text_form": self.form_class(),
            "title": self.title,
            **self.extra_context,
        }
        context.update(kwargs)
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        text_form = self.form_class(request.POST)
        if text_form.is_valid():
            return self.form_valid(text_form)
        else:
            return self.form_invalid()

    def form_valid(self, *args, **kwargs):
        raise NotImplementedError

    def form_invalid(self, **kwargs):
        context = {}
        context.update(kwargs)
        return render(
            self.request, self.template_name, self.get_context_data(**context)
        )
