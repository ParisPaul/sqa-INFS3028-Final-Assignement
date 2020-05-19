import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Testing class that execute the following tests
# - Test if POST work as intended
# - Test if the of the survey already exists
# - Test if the param is not included
class SurveyPOSTTests(APITestCase):

    # Called before executing each test
    def setUp(self):
        self.reference_data = {
            'name': 'test_dummy',
            'questions': [],
            'average': None,
            'standard_deviation': None,
            'minimum': None,
            'maximum': None
        }
        self.url = reverse('CreateSurveyView')

    # Called after executing each test
    def tearDown(self):
        self.client.delete(reverse('ResetSurveysListView'), {}, format='json')
    
    # Ensure that the route works as intended
    def test_success_create_survey(self):
        # Testing
        data = {
            'survey_name': 'test_dummy'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.reference_data)

    # Ensure the route returns 400 and error message if the template name already exist
    def test_fail_same_name(self):
        # Creating dummy data
        data = {
            'survey_name': 'test_dummy'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.reference_data)

        # Testing
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                "error": "survey name already exist, please choose a new one"
            }
        )

    # Ensure the route returns 400 and error message if 'survey_name' param is missing
    def test_fail_no_param(self):
        # Testing
        data = {
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "'survey_name' has to be a data param"
            }
        )


# Testing class that execute the following tests
# - Test if DELETE works as intended
class TestingHelpDELETETests(APITestCase):

    # Called before executing each test
    def setUp(self):
        self.reference_data = {
            'name': 'test_dummy',
            'questions': [],
            'average': None,
            'standard_deviation': None,
            'minimum': None,
            'maximum': None
        }
        self.url = reverse('ResetSurveysListView')

    # Called after executing each test
    def tearDown(self):
        self.client.delete(reverse('ResetSurveysListView'), {}, format='json')

    # Ensure the route works as intended
    def test_success_reset_surveys(self):
        # Creating dummy data
        data = {
            'survey_name': 'test_dummy'
        }
        response = self.client.post(reverse('CreateSurveyView'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.reference_data)

        # Testing
        data = {}
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})