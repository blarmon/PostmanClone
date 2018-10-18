from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import test, apiCall
from django.urls import reverse
import requests
from .forms import ApiForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    #form = ApiForm()
    current_user = request.user
    print(current_user)
    print(current_user.id)
    saved_calls = [i for i in apiCall.objects.filter(user = current_user.id)]
    context = {'testStuff': 'hey WORLD','saved_calls': saved_calls,}# 'form': form}
    return render(request, 'PostmanClone/index.html', context)

def submit(request):
    if 'submitButton' in request.POST:
        print("submit button")
        myTest = get_object_or_404(test, pk=1)
        baseURL = request.POST['baseURL']
        httpMethod = request.POST['httpMethod']
        headers = {}
        #make this thing its own method since you'll be doing shit with the headers all over the place!!!
        for i in range(3):
            index = i+1
            if (request.POST['headersa' + str(index)] != ""):
                headers[request.POST['headersa' + str(index)]] = request.POST['headersb' + str(index)]


        pythonCode = generatePythonCode(baseURL, httpMethod, headers)

        api_response = requests.request(httpMethod, baseURL, headers = headers).json()
        context = {'headers': headers, 'testObject': myTest, 'baseURL': baseURL, 'api_response': api_response, 'httpMethod': httpMethod, 'pythonCode': pythonCode}
        ##TODO: THIS NEEDS TO BE A REDIRECT!!!! if hettpmethod is post this needs to be a redirect.
        return render(request, 'PostmanClone/results.html', context)
    elif 'saveButton' in request.POST:
        print("save button")
        current_user = request.user
        #make a separate method that you pass POST into sometime to clean up this code!!  it can return your entire context
        baseURL = request.POST['baseURL']

        new_api_call = apiCall()
        new_api_call.base_url, new_api_call.headersa1, new_api_call.headersb1, new_api_call.headersa2, new_api_call.headersb2, new_api_call.headersa3, new_api_call.headersb3, new_api_call.httpMethod, new_api_call.user, new_api_call.name = request.POST['baseURL'], request.POST['headersa1'],request.POST['headersb1'], request.POST['headersa2'],request.POST['headersb2'], request.POST['headersa3'], request.POST['headersb3'], request.POST['httpMethod'], current_user, request.POST['api_call_name']
        new_api_call.save()
        return redirect('index')

def myregister(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html',context)


#method to be used in the submit view.  does this belong in another file by convention?
def generatePythonCode(baseURL, httpMethod, headers):
    pythonCode = "import requests\n\nbaseURL = \"" + baseURL + "\"\nhttpMethod = \"" + httpMethod + "\"\nheaders = " + str(headers) + "\n api_response = requests.request(httpMethod, baseURL, headers = headers).json()"


    #replace my newlines with actual newlines?
    pythonCode = pythonCode.replace(r'\n', '\n')
    return pythonCode