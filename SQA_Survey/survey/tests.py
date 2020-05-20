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
            'responses': [],
            'average': None,
            'standard_deviation': None,
            'minimum': None,
            'maximum': None
        }
        self.url = reverse('SurveyView')

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
# - Test if GET all survey work as intended
# - Test if GET one survey work as inteded
# - Test if the survey does not exist
class SurveyGETTest(APITestCase):

    # Called before executing each test
    def setUp(self):
        # Creating dummy data
        surveys = ['survey_1', 'survey_2', 'survey_3', 'survey_4', 'survey_5']
        for survey in surveys:
            data = {
                'survey_name': survey
            }
            self.client.post(reverse('SurveyView'), data, format='json')

        self.reference_data = {
            "question": "Do you like testing ?",
            "answers": [],
            "average": None,
            "standard_deviation": None,
            "minimum": None,
            "maximum": None
        }

        self.url_get_all = reverse('SurveyView')

    # Called after executing each test
    def tearDown(self):
        self.client.delete(reverse('ResetSurveysListView'), {}, format='json')

    # Ensure that the get all survey route is working as intended
    def test_sucess_list(self):
        # Testing
        response = self.client.get(self.url_get_all, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'surveys': [
                'survey_1',
                'survey_2',
                'survey_3',
                'survey_4',
                'survey_5'
                ]
            }
        )

    # Ensure that the Get one survey route works as entended
    def test_success_one_survey(self):
        # Testing
        data = {
            'survey_name': 'survey_1'
        }
        response = self.client.get(reverse('SurveyGETOneView', kwargs=data), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': 'survey_1',
            'questions': [],
            'responses': [],
            'average': None,
            'standard_deviation': None,
            'minimum': None,
            'maximum': None
        })
    
    def test_fail_survey_does_not_exist(self):
        # Testing
        data = {
            'survey_name': 'test_dummy'
        }
        response = self.client.get(reverse('SurveyGETOneView', kwargs=data), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'error': 'survey does not exist'
            }
        )


# Testing class that execute the following tests
# - Test if POST work as intended
# - Test if the 'survey_name' param is not included
# - Test if the 'question_text' param is not included
# - Test if no param is not included
# - Test if the survey does not exist
# - Test if the question already exist
# - Test if max question is reached
class QuestionPOSTTests(APITestCase):

    # Called before executing each test
    def setUp(self):
        # Creating dummy data
        data = {
            'survey_name': 'test_dummy'
        }
        self.client.post(reverse('SurveyView'), data, format='json')

        self.reference_data = {
            "question": "Do you like testing ?",
            "average": None,
            "standard_deviation": None,
            "minimum": None,
            "maximum": None
        }

        self.url = reverse('QuestionView')

    # Called after executing each test
    def tearDown(self):
        self.client.delete(reverse('ResetSurveysListView'), {}, format='json')

    # Ensure route is working as entended
    def test_success_create_question(self):
        # Testing
        data = {
            'survey_name': 'test_dummy',
            'question_text': 'Do you like testing ?'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.reference_data)
    
    # Ensure route returns 400 when 'survey_name' is not in param
    def test_fail_no_param_1(self):
        # Testing
        data = {
            'question_text': 'Do you like testing ?'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "'survey_name' has to be a data param"
            }
        )

    # Ensure route returns 400 when 'question_text' is not in param
    def test_fail_no_param_2(self):
        # Testing
        data = {
            'survey_name': 'test_dummy',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "'question_text' has to be a data param"
            }
        )

    # Ensure route returns 400 when there is no param
    def test_fail_no_param_3(self):
        # Testing
        data = {
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "'survey_name' has to be a data param"
            }
        )

    # Ensure route returns 400 when the survey does not exist
    def test_fail_survey_does_not_exist(self):
        # Delete all surveys
        self.client.delete(reverse('ResetSurveysListView'), {}, format='json')

        # Testing
        data = {
            'survey_name': 'test_dummy',
            'question_text': 'Do you like testing ?'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'error': 'survey does not exist'
            }
        )

    # Ensure route returns 400 when the question already exist
    def test_fail_question_already_exist(self):
        # Creating dummy data
        data = {
            'survey_name': 'test_dummy',
            'question_text': 'Do you like testing ?'
        }
        self.client.post(self.url, data, format='json')

        # Testing
        data = {
            'survey_name': 'test_dummy',
            'question_text': 'Do you like testing ?'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'error': 'question already exist, find a new one'
            }
        )
    
    # Ensure route returns 400 when the max number of questions is reached
    def test_fail_max_questions_reached(self):
        # Creating dummy data
        questions = ['1 ?', '2 ?', '3 ?', '4 ?', '5 ?', '6 ?', '7 ?', '8 ?', '9 ?', '10 ?']
        for question in questions:
            data = {
                'survey_name': 'test_dummy',
                'question_text': question
            }
            reference_data = {
                "question": question,
                "average": None,
                "standard_deviation": None,
                "minimum": None,
                "maximum": None
            }
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, reference_data)
        
        # Testing
        data = {
            'survey_name': 'test_dummy',
            'question_text': 'Do you like testing ?'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'error': 'you cannot add another question (maximum questions = 10)'
            }
        )


# Testing class that execute the following tests
# - Test if POST works as intended
# - Test if the survey exist
# - Test if there are questions to answer
# - Test if there is no argument
class SurveyResponsePOSTTests(APITestCase):

    # Called before executing each test
    def setUp(self):
        # Creating dummy data
        data = {
            'survey_name': 'test_dummy'
        }
        self.client.post(reverse('SurveyView'), data, format='json')
        questions = ['1 ?', '2 ?', '3 ?', '4 ?', '5 ?', '6 ?', '7 ?', '8 ?', '9 ?', '10 ?']
        for question in questions:
            data = {
                'survey_name': 'test_dummy',
                'question_text': question
            }
            self.client.post(reverse('QuestionView'), data, format='json')

        self.url = reverse('SurveyResponseView')

    # Called after executing each test
    def tearDown(self):
        self.client.delete(reverse('ResetSurveysListView'), {}, format='json')

    # Ensure the route works properly
    def test_success_create_survey_response(self):
        # Testing
        data = {
            'survey_name': 'test_dummy'
        }
        response = self.client.post(self.url, data, formet='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Ensure the route returns 400 when the survey does not exist
    def test_fail_survey_does_not_exist(self):
        # Testing
        data = {
            'survey_name': 'Hello_world'
        }
        response = self.client.post(self.url, data, formet='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': 'survey does not exist'
        })
    
    # Ensure the route returns 400 when there is no questions to answer
    def test_fail_no_question(self):
        # Create dummy data
        data = {
            'survey_name': 'Hello_World'
        }
        self.client.post(reverse('SurveyView'), data, format='json')

        #Testing
        data = {
            'survey_name': 'Hello_World'
        }
        response = self.client.post(self.url, data, formet='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': 'this survey has no questions'
        })
    
    # Ensure the route returns 400 when there is no argument given
    def test_fail_no_argument(self):
        #Testing
        data = {}
        response = self.client.post(self.url, data, formet='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "'survey_name' has to be a data param"
        })


# Testing class that execute the following tests
# - Test if UPDATE works as intended
# - Test if there is no param
# - Test if survey does not exist
# - Test if survey_response does not exist
# - Test if there is a question that is not supposed to be there or has been modified
# - Test if the questions have been answered with a number between 1 and 5
class SurveyResponseUPDATATests(APITestCase):

    # Called before executing each test
    def setUp(self):
        # Creating dummy data
        data = {
            'survey_name': 'test_dummy'
        }
        self.client.post(reverse('SurveyView'), data, format='json')
        questions = ['1 ?', '2 ?', '3 ?', '4 ?', '5 ?', '6 ?', '7 ?', '8 ?', '9 ?', '10 ?']
        for question in questions:
            data = {
                'survey_name': 'test_dummy',
                'question_text': question
            }
            self.client.post(reverse('QuestionView'), data, format='json')
        data = {
            'survey_name': 'test_dummy'
        }
        self.client.post(reverse('SurveyResponseView'), data, formet='json')

        self.url = reverse('SurveyResponseView')

    # Called after executing each test
    def tearDown(self):
        self.client.delete(reverse('ResetSurveysListView'), {}, format='json')
    
    # Ensure the route works as intended
    def test_success_update_survey_data(self):
        data = {
            'survey_response': {
                'id': '0',
                'survey_name': 'test_dummy',
                'description': 'Each questions can be answered with a number between 1 and 5 included.',
                'questions': {
                    '1 ?': 1,
                    '2 ?': 5,
                    '3 ?': 3,
                    '4 ?': 2,
                    '5 ?': 3,
                    '6 ?': 1,
                    '7 ?': 5,
                    '8 ?': 3,
                    '9 ?': 2,
                    '10 ?': 1
                }
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': '0',
            'survey_name': 'test_dummy',
            'description': 'Each questions can be answered with a number between 1 and 5 included.',
            'questions': {
                '1 ?': 1,
                '2 ?': 5,
                '3 ?': 3,
                '4 ?': 2,
                '5 ?': 3,
                '6 ?': 1,
                '7 ?': 5,
                '8 ?': 3,
                '9 ?': 2,
                '10 ?': 1
            }
        })

    # Ensure the route returns 400 when there is no param
    def test_fail_no_param(self):
        data = {}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "'survey_response' has to be a data param"
        })

    # Ensure the route returns 400 when the survey does not exist
    def test_fail_survey_does_not_exist(self):
        data = {
            'survey_response': {
                'id': '0',
                'survey_name': 'nope',
                'description': 'Each questions can be answered with a number between 1 and 5 included.',
                'questions': {
                    '1 ?': 1,
                    '2 ?': 5,
                    '3 ?': 3,
                    '4 ?': 2,
                    '5 ?': 3,
                    'This is wrong': 1,
                    '7 ?': 5,
                    '8 ?': 3,
                    '9 ?': 2,
                    '10 ?': 1
                }
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': 'survey does not exist, name may be wrong'
        })

    # Ensure the route returns 400 when the survey response id could not be match, meaning the survey response does not exist
    def test_fail_survey_response_does_not_exist(self):
        data = {
            'survey_response': {
                'id': '-1',
                'survey_name': 'test_dummy',
                'description': 'Each questions can be answered with a number between 1 and 5 included.',
                'questions': {
                    '1 ?': 1,
                    '2 ?': 5,
                    '3 ?': 3,
                    '4 ?': 2,
                    '5 ?': 3,
                    'This is wrong': 1,
                    '7 ?': 5,
                    '8 ?': 3,
                    '9 ?': 2,
                    '10 ?': 1
                }
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': 'survey response does not exist, it may be wrong'
        })

    # Ensure the route return 400 if one question was mofified in the json
    def test_fail_question_replaced(self):
        data = {
            'survey_response': {
                'id': '0',
                'survey_name': 'test_dummy',
                'description': 'Each questions can be answered with a number between 1 and 5 included.',
                'questions': {
                    '1 ?': 1,
                    '2 ?': 5,
                    '3 ?': 3,
                    '4 ?': 2,
                    '5 ?': 3,
                    'This is wrong': 1,
                    '7 ?': 5,
                    '8 ?': 3,
                    '9 ?': 2,
                    '10 ?': 1
                }
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "the question 'This is wrong' does not exist OR the number is not between 1 and 5"
        })

    # Ensure the route return 400 if one question was mofified in the json
    def test_fail_question_replaced_2(self):
        data = {
            'survey_response': {
                'id': '0',
                'survey_name': 'test_dummy',
                'description': 'Each questions can be answered with a number between 1 and 5 included.',
                'questions': {
                    '1 ?': 1,
                    '5 ?': 3,
                    'This is wrong': 1,
                    '7 ?': 5,
                    '8 ?': 3,
                    '9 ?': 2,
                    '10 ?': 1
                }
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "the question 'This is wrong' does not exist OR the number is not between 1 and 5"
        })

    # Ensure the route return 400 if the number is not between 1 and 5 included
    def test_fail_question_replaced_3(self):
        data = {
            'survey_response': {
                'id': '0',
                'survey_name': 'test_dummy',
                'description': 'Each questions can be answered with a number between 1 and 5 included.',
                'questions': {
                    '1 ?': 1,
                    '5 ?': 3,
                    '6 ?': 1,
                    '7 ?': 8,
                    '8 ?': 3,
                    '9 ?': 2,
                    '10 ?': 1
                }
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "the question '7 ?' does not exist OR the number is not between 1 and 5"
        })

    # Ensure the route return 400 if the number is not between 1 and 5 included
    def test_fail_question_replaced_4(self):
        data = {
            'survey_response': {
                'id': '0',
                'survey_name': 'test_dummy',
                'description': 'Each questions can be answered with a number between 1 and 5 included.',
                'questions': {
                    '1 ?': 1,
                    '5 ?': 3,
                    '6 ?': 1,
                    '7 ?': 5,
                    '8 ?': 3,
                    '9 ?': 2,
                    '10 ?': -543
                }
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': "the question '10 ?' does not exist OR the number is not between 1 and 5"
    })


# Testing class that execute the following tests
# - Test if DELETE works as intended
class TestingHelpDELETETests(APITestCase):

    # Called before executing each test
    def setUp(self):
        self.reference_data = {
            'name': 'test_dummy',
            'questions': [],
            'responses': [],
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
        response = self.client.post(reverse('SurveyView'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.reference_data)

        # Testing
        data = {}
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})