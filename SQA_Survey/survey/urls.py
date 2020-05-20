from django.urls import path

from . import views

urlpatterns = [
    path('survey/', views.SurveyView.as_view(), name='SurveyView'),
    path('question/', views.QuestionView.as_view(), name='QuestionView'),
    path('reset_surveys/', views.TestingHelp.as_view(), name='ResetSurveysListView')
]
