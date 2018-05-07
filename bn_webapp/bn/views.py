from django.shortcuts import render
from django.http import HttpResponse
from bn.bn_model import get_users_depression_rate

def index(request):
    return HttpResponse(get_users_depression_rate())
