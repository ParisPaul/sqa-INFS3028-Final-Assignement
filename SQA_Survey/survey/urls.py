from django.urls import path

from . import views

urlpatterns = [
    # Survey
    path('survey/', views.SurveyView.as_view(), name='SurveyView'),
    path('survey/<str:survey_name>/', views.ComplementSurveyView.as_view(), name='SurveyGETOneView'),

    # Question
    path('question/', views.QuestionView.as_view(), name='QuestionView'),

    # Survey Response
    path('survey_response/', views.SurveyResponseView.as_view(), name='SurveyResponseView'),
    path('survey_response/<str:survey_name>/', views.SurveyResponseView.as_view(), name='SurveyResponseView'),

    # Testing
    path('reset_surveys/', views.TestingHelp.as_view(), name='ResetSurveysListView')
]
