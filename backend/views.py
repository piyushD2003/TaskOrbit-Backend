from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HomeView(APIView):
    def get(self,request):
        data = {"message": "Hello, World Home!"}
            # return HttpResponse("Hello world about")
        return Response(data, status=status.HTTP_200_OK)
