from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import test, apiCall, Collection
from django.urls import reverse
import requests, ast
from .forms import ApiForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail

# Create your views here.
def index(request):
    context = {}
    if request.method == "POST":
        baseURL = request.POST['baseURL']
        httpMethod = request.POST['httpMethod']
        headers = {}
        # make this thing its own method since you'll be doing shit with the headers all over the place!!!
        for i in range(3):
            index = i + 1
            if (request.POST['headersa' + str(index)] != ""):
                headers[request.POST['headersa' + str(index)]] = request.POST['headersb' + str(index)]
        api_response = requests.request(httpMethod, baseURL, headers=headers).json()
        pythonCode = generatePythonCode(baseURL, httpMethod, headers)
        contextAddition = {'baseURL': baseURL, 'httpMethod': httpMethod, 'headers': headers, 'apiResponse': api_response, 'pythonCode': pythonCode}
        context.update(contextAddition)

    current_user = request.user
    user_collections = [i for i in Collection.objects.filter(user = current_user.id)]
    #hash table to store calls and connect them to a certain collection!!!
    user_calls = []
    current_collection_name = None
    if 'collection' not in request.session:
        pass
    else:
        #this is definitely an unnecessary DB call, try to eliminate this if possible...
        current_collection_name = request.session['collection']
        current_session_collection = get_object_or_404(Collection, name = request.session['collection'])
        user_calls.append(apiCall.objects.filter(collection = current_session_collection))

    context.update({'user_collections': user_collections, 'user_calls': user_calls, 'current_collection_name': current_collection_name})
    return render(request, 'PostmanClone/index.html', context)

def submit(request):
    if 'saveButton' in request.POST:
        current_user = request.user
        current_collection = get_object_or_404(Collection, name=request.session['collection'])
        headers = ast.literal_eval((request.POST['headers']))
        print(headers)
        headersList = ["" for i in range(6)]
        count = 0
        for key, value in headers.items():
            # headersList.append(key)
            # headersList.append(value)
            headersList[count] = key
            count += 1
            headersList[count] = value
            count += 1
        print(headersList)
        #make a separate method that you pass POST into sometime to clean up this code!!  it can return your entire context
        new_api_call = apiCall()
        new_api_call.base_url, new_api_call.headersa1, new_api_call.headersb1, new_api_call.headersa2, new_api_call.headersb2, new_api_call.headersa3, new_api_call.headersb3, new_api_call.httpMethod, new_api_call.collection, new_api_call.name = request.POST['baseURL'], headersList[0], headersList[1], headersList[2], headersList[3], headersList[4], headersList[5], request.POST['httpMethod'], current_collection, request.POST['api_call_name']
        new_api_call.save()
        return redirect('index')

def emailThankYou(request):
    return render(request, 'PostmanClone/thankyouemail.html')

def changeCollection(request):
    if request.POST['collection'] == 'newCollection':
        newCollection = Collection(name=request.POST['newCollectionName'], user = request.user)
        newCollection.save()
        request.session['collection'] = request.POST['newCollectionName']
    else:
        request.session['collection'] = request.POST['collection']
    return redirect('index')

def contact(request):
    if request.method == 'POST':
        #figure this part out later! TODO
        return redirect('thanks')
        # send_mail(
        #     request.POST['subject'],
        #     request.POST['content'],
        #     request.POST['fromEmail'],
        #     ['c.siegel1991@gmail.com'],
        #     fail_silently=False,
        # )
        #return redirect('index')
    else:
        return render(request, 'PostmanClone/contactform.html')

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