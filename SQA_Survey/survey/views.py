from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4

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
                'answers': [],
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
# - DELETE: Reset the serveys list
class TestingHelp(APIView):

    global surveys

    # reset the servey list for testing
    def delete(self, request, format=None):
        surveys.clear()
        return Response({}, status=status.HTTP_200_OK)
