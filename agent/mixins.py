from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganizerAndLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role == "organizer":
            return redirect("leads:home_page")
        return super().dispatch(request, *args, **kwargs)
