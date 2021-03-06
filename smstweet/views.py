from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from xml.dom import minidom
from smstweet.models import *
import datetime

def updateIncomingText(entry):
    new = IncomingText(msgType = entry['messageType'],
                    msgId = entry['id'],
                    source = entry['source'],
                    target = entry['target'],
                    msg = entry['msg'],
                    udh = entry['udh'])
    new.save()

@csrf_exempt
def process(request):
    if request.method != 'POST':
        raise Http404
    dom = minidom.parseString(request.body)
    xmlList = dom.getElementsByTagName('param')
    entry = {}
    for i in xmlList:
        name = i.getElementsByTagName('name')[0].childNodes[0]
        try:
            value = i.getElementsByTagName('value')[0].childNodes[0]
        except IndexError:
            entry[name.nodeValue] = ''
        else:
            entry[name.nodeValue] = value.nodeValue
    updateIncomingText(entry)
    return HttpResponse()

@csrf_exempt
def update(request):
    '''
    TODO: update method to return a list of new IncomingText
    entries given a specified time from POST
    '''
    if request.method != 'POST':
        raise Http404
    data = request.POST['time']
    latest = IncomingText.objects.latest('timestamp')
    return HttpResponse(data)

def show(request):
    text_list = IncomingText.objects.all()
    rendered = int(datetime.datetime.now().strftime('%s'))
    return render_to_response('index.html', {'texts': text_list,
            'render': rendered})
