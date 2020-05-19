from django.urls import path

from . import views

urlpatterns = [
    path('survey/', views.SurveyView.as_view(), name='CreateSurveyView'),
    path('reset_surveys/', views.TestingHelp.as_view(), name='ResetSurveysListView')
]
