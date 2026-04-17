from django.shortcuts import reverse
from .models import Lead, Category
from .forms import (
    LeadModelForm,
    CustomUserCreationForm,
    LeadCategoryUpdateForm,
    CreateCategoryForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from agent.mixins import OrganizerAndLoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import generic
from django.db.models import Count


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("leads:home_page")


class LeadListView(LoginRequiredMixin, ListView):
    template_name = "home_page.html"
    context_object_name = "leads"

    def get_queryset(self):
        request = self.request
        query = request.GET.get("search")

        if request.user.role == "organizer":
            queryset = Lead.objects.filter(owner=request.user, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                owner=request.user.manager.owner, agent__manager=request.user
            )

        if query:
            queryset = queryset.filter(first_name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        request = self.request
        query = request.GET.get("search_unassigned")
        if request.user.role == "organizer":
            queryset = Lead.objects.filter(owner=request.user, agent__isnull=True)
            context.update({"unassigned_leads": queryset})
            if query:
                queryset = queryset.filter(first_name__icontains=query)
                context.update({"unassigned_leads": queryset})
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = "create_lead.html"
    form_class = LeadModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        if self.request.user.role == "organizer":
            form.instance.owner = self.request.user
        else:
            form.instance.agent = self.request.user.manager
            form.instance.owner = self.request.user.manager.owner
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("leads:home_page")


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "update_lead.html"
    form_class = LeadModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_queryset(self):
        user = self.request.user

        if user.role == "organizer":
            return Lead.objects.filter(owner=user)
        else:
            return Lead.objects.filter(owner=user.manager.owner, agent__manager=user)

    def get_success_url(self):
        return reverse("leads:home_page")


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "delete_lead.html"

    def get_queryset(self):
        user = self.request.user

        if user.role == "organizer":
            return Lead.objects.filter(owner=user)
        else:
            return Lead.objects.filter(owner=user.manager.owner, agent__manager=user)

    def get_success_url(self):
        return reverse("leads:home_page")


class CategoryListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        queryset = Lead.objects.filter(owner=user)

        context.update(
            {
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
            }
        )
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(owner=user)
        return queryset.annotate(lead_count=Count("leads"))


class CategoryDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()
        context.update({"leads": leads})
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(owner=user)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if user.role == "organizer":
            queryset = Lead.objects.filter(owner=user)
        else:
            queryset = Lead.objects.filter(
                owner=user.manager.owner, agent__manager=user
            )
        return queryset

    def get_success_url(self):
        return reverse("leads:home_page")


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "create_category.html"
    form_class = CreateCategoryForm
    model = Category

    def form_valid(self, form):
        user = self.request.user
        if user.role == "organizer":
            form.instance.owner = user
        else:
            form.instance.owner = user.manager.owner
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("leads:home_page")
