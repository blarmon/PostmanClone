from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import test
from django.urls import reverse
import requests


# Create your views here.
def index(request):
    context = {'testStuff': 'hey WORLD'}
    return render(request, 'PostmanClone/index.html', context)

def submit(request):
    myTest = get_object_or_404(test, pk=1)
    baseURL = request.POST['baseURL']
    httpMethod = request.POST['httpMethod']
    headers = {}
    for i in range(3):
        index = i+1
        if (request.POST['headersa' + str(index)] != ""):
            headers[request.POST['headersa' + str(index)]] = request.POST['headersb' + str(index)]


    pythonCode = generatePythonCode(baseURL, httpMethod, headers)

    api_response = requests.request(httpMethod, baseURL, headers = headers).json()
    context = {'headers': headers, 'testObject': myTest, 'baseURL': baseURL, 'api_response': api_response, 'httpMethod': httpMethod, 'pythonCode': pythonCode}
    ##TODO: THIS NEEDS TO BE A REDIRECT!!!! if hettpmethod is post this needs to be a redirect.
    return render(request, 'PostmanClone/results.html', context)

#method to be used in the submit view.  does this belong in another file by convention?
def generatePythonCode(baseURL, httpMethod, headers):
    pythonCode = "import requests\n\nbaseURL = \"" + baseURL + "\"\nhttpMethod = \"" + httpMethod + "\"\nheaders = " + str(headers) + "\n api_response = requests.request(httpMethod, baseURL, headers = headers).json()"


    #replace my newlines with actual newlines?
    pythonCode = pythonCode.replace(r'\n', '\n')
    return pythonCode