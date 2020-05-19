from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4

# Global variable storing the surveys
surveys = []

# View that handles the following routes:
# - POST: Create a survey
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
        if self.findSurvey(survey_name) != None:
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
        response = self.findSurvey(survey_name)
        return Response(response, status=status.HTTP_201_CREATED)

    # Function to find any survey from their name
    def findSurvey(self, name):
        for survey in surveys:
            if survey['name'] == name:
                return survey
        return None

# View that handles the following routes:
# - DELETE: Reset the serveys list
class TestingHelp(APIView):

    global surveys

    # reset the servey list for testing
    def delete(self, request, format=None):
        surveys.clear()
        return Response({}, status=status.HTTP_200_OK)
