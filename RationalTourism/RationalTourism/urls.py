"""RationalTourism URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from RationalTourism import views

urlpatterns = [
    path('', views.index),
    path('startGame', views.start_game),
    path('endGame', views.end_game),
    path('setUsername', views.set_username),
    path('resetUsers', views.reset_users),
    path('ranking', views.ranking),
    path('getPointsOfInterest', views.get_points_of_interest),
    path('getRandomPoi', views.get_random_poi),
    path('submitPhaseOne', views.submit_phase_one),
    path('getTargetLocation', views.get_target_location),
    path('phaseTwo', views.generate_phase2),
    path('submitPhaseTwo', views.submit_phase2),
    path('phaseThree', views.generate_phase3),
    path('submitPhaseThree', views.submit_phase3),
    path('phaseTwoInfo', views.phase2_info),
    path('phaseThreeInfo', views.phase3_info),
    path('getLevel', views.get_level),
]
