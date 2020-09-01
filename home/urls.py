from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('managers/home', views.managers, name='managers'),
    path('agents/home', views.agents, name='agents'),
    path('manage/agents', views.manage_agents, name='manage_agents'),
    path('redirect', views.decider, name='decider'),

]
