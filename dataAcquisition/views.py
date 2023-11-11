from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from multiprocessing import Process
from multiprocessing.sharedctypes import Value
from .service.src.SystemStart import run

trafficLightColor = Value('i', 2, lock=False)
face = Value('i', 0)
p = Process(target=run, args=(trafficLightColor, face))
p.start()

class Post_APIView(APIView):
    def parseColor(self, color):
        if color == 0:
            return 'green'
        if color == 1:
            return 'yellow'
        if color == 2:
            return 'red'
    def get(self, request, format=None, *args, **kwargs):
        # tmp = request.data.get('width')
        
        response_data = {}
        # response_data['result'] = 'working...'
        response_data['color'] = self.parseColor(trafficLightColor.value)
        response_data['face'] = face.value
        return JsonResponse(response_data)

    def post(self, request, format=None):
        tmp = request.data.get('width')
        print(tmp)
        
# subprocess.run(["python3", os.getcwd()+"/dataAcquisition/Server_Data.py"], stdout=subprocess.PIPE)
