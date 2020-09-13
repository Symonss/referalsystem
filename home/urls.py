from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('managers/home', views.managers, name='managers'),
    path('agents/pp', views.agents, name='agents'),
    path('agents/home', views.agents_home, name='agents-index'),
    path('manage/agents', views.manage_agents, name='manage_agents'),
    path('redirect', views.decider, name='decider'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
