from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.views import APIView

from rest_framework.response import Response

from django.http import HttpResponse

from django.http import JsonResponse
import time

class Post_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        # tmp = request.data.get('width')
        response_data = {}
        response_data['result'] = 'working...'
        response_data['color'] = 'red'
        response_data['face'] = True
        time.sleep(2)

        return JsonResponse(response_data)

    def post(self, request, format=None):
        tmp = request.data.get('width')
        print(tmp)
        
        # return Response(serializer.data)