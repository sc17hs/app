# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Module, Professor, Rating, User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from decimal import *
from django.contrib.auth import login,logout
from rest_framework.authtoken.models import Token
import io
from rest_framework.permissions import IsAuthenticated


# Create your views here.

# Lists all modules

import json
from django.core import serializers



class ModuleList(APIView):

    def get(self, request):
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        serializer_data = serializer.data

        return Response(serializer_data)


class ProfessorList(APIView):

    def get(self, request):
        professors = Professor.objects.all()
        serializer = ProfessorSerializer(professors, many=True)
        return Response(serializer.data)


def view(request):
    lecturers = Professor.objects.all().values()
    lecturers_list = list(lecturers)
    ratings = Rating.objects.all().values()
    ratings_list = list(ratings)
    for x in lecturers_list:
        num_of_ratings = 0
        total = 0
        for z in ratings_list:
            if z['professorid_id']==x['code']:
                num_of_ratings = num_of_ratings +1
                total = total+z['rating']

        if num_of_ratings ==0:
            x['rating'] = 0
        else:

            av = float(total)/float(num_of_ratings)
            #print('total = '+str(total))
            #print('number of ratings = '+ str(num_of_ratings))
            #print('average = '+ str(av))
            x['rating'] = int(round(av))
        #print(x)

    return JsonResponse(lecturers_list, safe=False)


def average(request,profid,modid):
    lecturers = Professor.objects.filter(code=profid).values()
    lecturers_list = list(lecturers)
    ratings = Rating.objects.filter(module_code__code=modid).values()
    ratings_list = list(ratings)
    # print(ratings_list)
    for x in lecturers_list:
        num_of_ratings = 0
        total = 0
        for z in ratings_list:
            if z['professorid_id']==x['code']:
                num_of_ratings = num_of_ratings +1
                total = total+z['rating']
                #print(total)

        if num_of_ratings ==0:
            x['rating'] = 0
        else:
            rate = float(total)/num_of_ratings
            averageRating = Decimal(rate).quantize(Decimal('0'), ROUND_HALF_UP)
            x['rating'] = averageRating
            # print(averageRating)
        # print(x)


    return JsonResponse(lecturers_list, safe=False)


class CreateUserView(CreateAPIView):
    model = User
    serializer_class = UserSerializer


class CreateRatingView(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self,request):

        data = io.BytesIO(request.body)
        parsed = JSONParser().parse(data)
        serialized = RatingSerializer(data= parsed)
        serialized.is_valid()

        professor = serialized.validated_data.get('professorid')
        module_id= serialized.validated_data.get('module_code')
        year = serialized.validated_data.get('year')
        rating = serialized.validated_data.get('rating')

        professor_code = Professor.objects.get(code=professor)
        module_code = Module.objects.get(code=module_id, year=year)
        rating = Rating.objects.create(
            professorid=professor_code,
            module_code = module_code,
            year = year,
            rating = rating,
        )

        rating.save()
        jsonResponse = str(rating)
        return Response(jsonResponse)

class LoginView(APIView):

    def post(self,request):
        data = io.BytesIO(request.body)
        parsed = JSONParser().parse(data)
        serialized = LoginSerializer(data= parsed)
        serialized.is_valid()

        username = serialized.validated_data.get('username')
        password= serialized.validated_data.get('password')

        user = User.objects.get(username = username)

        if user.password == password:
            print("USER AUTHENTICATED")
            login(request,user)
            token = Token.objects.get_or_create(user = user)
            #print(token[0])
            #(user.is_authenticated)
        else:
            return Response("Incorrect Credentials")
        #print(user)
        tokenval = token[0]
        tokenval = str(tokenval)
        #print(type(tokenval))

        return Response({"token": tokenval})

