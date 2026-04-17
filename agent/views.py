from django.core.mail import send_mail
import logging
from django.shortcuts import reverse, redirect
from django.views import generic
from .models import Agent
from leads.models import Manager
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin

logger = logging.getLogger(__name__)


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        return Agent.objects.filter(owner=self.request.user)


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/create_agent.html"
    form_class = AgentModelForm
    model = Manager

    def form_valid(self, form):
        manager = form.save(commit=False)
        manager.role = "agent"

        manager.save()
        Agent.objects.create(
            manager=manager,
            owner=self.request.user,
        )
        try:
            send_mail(
                subject="Invitation to join as an Agent",
                message="You were added as an agent on DJCRM",
                from_email=self.request.user.username,
                recipient_list=[manager.email],
            )
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
        return redirect("agent:agents")


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Agent.objects.filter(owner=self.request.user)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/update_agent.html"
    form_class = AgentModelForm

    def get_queryset(self):
        return Agent.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object().manager
        return kwargs

    def get_success_url(self):
        return reverse("agent:agents")


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"

    def get_success_url(self):
        return reverse("agent:agents")

    def get_queryset(self):
        return Agent.objects.filter(owner=self.request.user)
