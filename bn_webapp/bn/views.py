from django.shortcuts import render
from django.http import HttpResponse
from bn.bn_model import get_users_depression_rate

def index(request):

    html = '<table style="width:100%; text-align: center;"><tr><th>USER NAME</th><th>DEPRESSION RATE</th></tr>';
    data = get_users_depression_rate()
    for d in data:
        html += "<tr>"
        html += '<td>{}</td>'.format(d['user_name'])
        html += '<td>{}</td>'.format(d['depression_rate'])
        html += "</tr>"

    html += "</table>"
    return HttpResponse(html)
