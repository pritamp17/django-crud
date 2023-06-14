from rest_framework.views import APIView
from rest_framework.response import Response



class WelcomeView(APIView):
     def get(self, request):
          return Response({'Welcome': 'try {localhost/api/login} '})