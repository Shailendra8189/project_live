from django.urls import path
from .views import (
    AgentListView,
    AgentCreateView,
    AgentDetailView,
    AgentUpdateView,
    AgentDeleteView,
)

app_name = "agent"

urlpatterns = [
    path("", AgentListView.as_view(), name="agents"),
    path("create/", AgentCreateView.as_view(), name="create_agent"),
    path("<int:pk>/", AgentDetailView.as_view(), name="agent_detail"),
    path("<int:pk>/update/", AgentUpdateView.as_view(), name="update_agent"),
    path("<int:pk>/delete/", AgentDeleteView.as_view(), name="delete_agent"),
]
