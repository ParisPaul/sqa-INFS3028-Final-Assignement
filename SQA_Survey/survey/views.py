from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from statistics import stdev
import time
import json

# Global variable storing the surveys
surveys = []

# View that handles the following routes:
# - POST: Create a survey
# - GET: Get a list of names of all the existing surveys
class SurveyView(APIView):

    global surveys

    # Create a survey
    def post(self, request, format=None):
        try:
            survey_name = request.data['survey_name']
        except KeyError as e:
            response = {
                'error': str(e) + ' has to be a data param'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if self.findSurveyIndex(survey_name) != None:
            response = {
                'error': 'survey name already exist, please choose a new one'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        surveys.append(
            {
                'name': survey_name,
                'questions': [],
                'responses': [],
                'average': None,
                'standard_deviation': None,
                'minimum': None,
                'maximum': None
            }
        )
        response = surveys[self.findSurveyIndex(survey_name)]
        return Response(response, status=status.HTTP_201_CREATED)

    # Return a list of the names of all surveys
    def get(self, request, format=None):
        response = {
            'surveys': []
        }
        for survey in surveys:
            response['surveys'].append(survey['name'])
        return Response(response, status=status.HTTP_200_OK)

    # Function to find any survey from their name
    def findSurveyIndex(self, name):
        for index, survey in enumerate(surveys):
            if survey['name'] == name:
                return index
        return None


# View that handles the following routes:
# - GET: get all information about one servey
class ComplementSurveyView(APIView):

    global surveys

    # Return the survey object of the desired survey
    def get(self, request, survey_name, format=None):
        survey_index = self.findSurveyIndex(survey_name)
        if survey_index == None:
            response = {
                'error': 'survey does not exist'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = surveys[survey_index]
        return Response(response, status=status.HTTP_200_OK)

    # Function to find any survey from their name
    def findSurveyIndex(self, name):
        for index, survey in enumerate(surveys):
            if survey['name'] == name:
                return index
        return None


# View that handles the following routes:
# - POST: Create and add a question to an existing survey
class QuestionView(APIView):

    global surveys

    # Add a question to a given survey
    def post(self, request, format=None):
        try:
            survey_name = request.data['survey_name']
            question_text = request.data['question_text']
        except KeyError as e:
            response = {
                'error': str(e) + ' has to be a data param'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        survey_index = self.findSurveyIndex(survey_name)
        if survey_index == None:
            response = {
                'error': 'survey does not exist'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if self.findQuestionIndex(survey_index, question_text) != None:
            response = {
                'error': 'question already exist, find a new one'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if len(surveys[survey_index]['questions']) >= 10:
            response = {
                'error': 'you cannot add another question (maximum questions = 10)'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        surveys[survey_index]['questions'].append(
            {
                'question': question_text,
                'average': None,
                'standard_deviation': None,
                'minimum': None,
                'maximum': None
            }
        )
        response = surveys[survey_index]['questions'][self.findQuestionIndex(survey_index, question_text)]
        return Response(response, status=status.HTTP_201_CREATED)

    # Function to find any survey from their name
    def findSurveyIndex(self, name):
        for index, survey in enumerate(surveys):
            if survey['name'] == name:
                return index
        return None
    
    # Function to find any question from their name
    def findQuestionIndex(self, survey_index, question_text):
        for index, question in enumerate(surveys[survey_index]['questions']):
            if question['question'] == question_text:
                return index
        return None

# View that handles the following routes:
# - POST: Create a survey response linked to the desired survey
# - UPDATE: Add answer to one of the questions
# - GET: Get all survey responses from a desired survey
class SurveyResponseView(APIView):

    global surveys

    # Create a survey response
    def post(self, request, format=None):
        try:
            survey_name = request.data['survey_name']
        except KeyError as e:
            response = {
                'error': str(e) + ' has to be a data param'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        survey_index = self.findSurveyIndex(survey_name)
        if survey_index == None:
            response = {
                'error': 'survey does not exist'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if len(surveys[survey_index]['questions']) == 0:
            response = {
                'error': 'this survey has no questions'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {
            'id': str(round(time.time() * 1000)),
            'survey_name': survey_name,
            'description': 'Each questions can be answered with a number between 1 and 5 included.',
            'questions': {}
        }
        for question in surveys[survey_index]['questions']:
            response['questions'][question['question']] = None
        surveys[survey_index]['responses'].append(response)
        return Response(response, status=status.HTTP_201_CREATED)

    # Update the survey response
    def patch(self, request, format=None):
        try:
            survey_response = request.data['survey_response']
        except KeyError as e:
            response = {
                'error': str(e) + ' has to be a data param'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        survey_name = survey_response['survey_name']
        id = survey_response['id']
        survey_index = self.findSurveyIndex(survey_name)
        if survey_index == None:
            response = {
                'error': 'survey does not exist, name may be wrong'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        survey_response_index = self.findSurveyResponseIndex(id, survey_index)
        if survey_response_index == None:
            response = {
                'error': 'survey response does not exist, it may be wrong'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        for response, value in survey_response['questions'].items():
            if self.findQuestionIndex(survey_index, response) == None or value < 1 or value > 5:
                response = {
                    'error': 'the question \'' + str(response) +'\' does not exist OR the number is not between 1 and 5'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        surveys[survey_index]['responses'][survey_response_index] = survey_response
        self.calculate_stats(survey_index)
        response = surveys[survey_index]['responses'][survey_response_index]
        return Response(response, status=status.HTTP_200_OK)

    # Get all survey responses from one survey
    def get(self, request, survey_name, format=None):
        survey_index = self.findSurveyIndex(survey_name)
        if survey_index == None:
            response = {
                'error': 'survey does not exist'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        resp = {
            'survey_responses': []
        }
        for response in surveys[survey_index]['responses']:
            resp['survey_responses'].append(response)
        return Response(resp, status=status.HTTP_200_OK)

    # Function to find any survey from their name
    def findSurveyIndex(self, name):
        for index, survey in enumerate(surveys):
            if survey['name'] == name:
                return index
        return None

    # Function to find any survey response with the id
    def findSurveyResponseIndex(self, id, survey_index):
        for index, response in enumerate(surveys[survey_index]['responses']):
            if response['id'] == id:
                return index
        return None
    
    # Function to find any question from their name
    def findQuestionIndex(self, survey_index, question_text):
        for index, question in enumerate(surveys[survey_index]['questions']):
            if str(question['question']) == question_text:
                return index
        return None
    
    # calculate the stats for each questions and the survey as a whole
    def calculate_stats(self, survey_index):
        survey_stat = []
        questions_stat = dict()
        for question in surveys[survey_index]['questions']:
            questions_stat[question['question']] = []
        for response in surveys[survey_index]['responses']:
            for resp, value in response['questions'].items():
                if isinstance(value, int) or isinstance(value, str):
                    questions_stat[resp].append(int(value))
                    survey_stat.append(int(value))
        for index, question in enumerate(surveys[survey_index]['questions']):
            if len(questions_stat[question['question']]) != 0:
                surveys[survey_index]['questions'][index]['average'] = sum(questions_stat[question['question']]) / len(questions_stat[question['question']])
                surveys[survey_index]['questions'][index]['minimum'] = min(questions_stat[question['question']])
                surveys[survey_index]['questions'][index]['maximum'] = max(questions_stat[question['question']])
            if len(questions_stat[question['question']]) >= 2:
                surveys[survey_index]['questions'][index]['standard_deviation'] = stdev(questions_stat[question['question']])
        if len(survey_stat) != 0:
            surveys[survey_index]['average'] = sum(survey_stat) / len(survey_stat)
            surveys[survey_index]['minimum'] = min(survey_stat)
            surveys[survey_index]['maximum'] = max(survey_stat)
        if len(survey_stat) >= 2:
            surveys[survey_index]['standard_deviation'] = stdev(survey_stat)


# View that handles the following routes:
# - DELETE: Reset the serveys list
class TestingHelp(APIView):

    global surveys

    # reset the servey list for testing
    def delete(self, request, format=None):
        surveys.clear()
        return Response({}, status=status.HTTP_200_OK)
