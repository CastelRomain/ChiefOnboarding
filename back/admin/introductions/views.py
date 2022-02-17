from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from users.mixins import AdminPermMixin, LoginRequiredMixin
from users.models import User

from .forms import IntroductionForm
from .models import Introduction
from django.utils.translation import gettext as _


class IntroductionListView(LoginRequiredMixin, AdminPermMixin, ListView):
    template_name = "templates.html"
    queryset = Introduction.templates.all().order_by("name")
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Introduction items")
        context["subtitle"] = _("templates")
        context["add_action"] = reverse_lazy("introductions:create")
        return context


class IntroductionCreateView(
    LoginRequiredMixin, AdminPermMixin, SuccessMessageMixin, CreateView
):
    template_name = "todo_update.html"
    form_class = IntroductionForm
    success_url = reverse_lazy("introductions:list")
    success_message = _("Introduction item has been updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create introduction item")
        context["subtitle"] = _("templates")
        return context


class IntroductionColleaguePreviewView(LoginRequiredMixin, AdminPermMixin, DetailView):
    template_name = "_colleague_intro.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["intro_person"] = context["object"]
        return context


class IntroductionUpdateView(
    LoginRequiredMixin, AdminPermMixin, SuccessMessageMixin, UpdateView
):
    template_name = "intro_update.html"
    form_class = IntroductionForm
    success_url = reverse_lazy("introductions:list")
    queryset = Introduction.templates.all()
    success_message = _("Introduction item has been updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update introduction item")
        context["subtitle"] = _("templates")
        return context


class IntroductionDeleteView(LoginRequiredMixin, AdminPermMixin, DeleteView):
    queryset = Introduction.objects.all()
    success_url = reverse_lazy("introductions:list")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(request, _("Introduction item has been removed"))
        return response
