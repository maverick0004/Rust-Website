from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadImage
from django.http import HttpResponse
import os
import base64
import requests
import json
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'upload.html')

def upload(request):
    if request.method == 'POST':
        #form = UploadImage(request.POST,request.FILES)
        #if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location='./')
        filename = fs.save(myfile.name, myfile)
    
        # # cd = form.cleaned_data
        # # myfile=cd['file']
        #myfile = form.file
        filename = './'+myfile.name
        with open(filename, 'rb') as file:
            encoded = base64.b64encode(file.read())
        img_dict = {filename: encoded.decode('utf-8')}
        body = json.dumps(img_dict)
        headers = {'Content-Type':'application/json'}
        response = requests.post('http://104.45.69.38:80/score', headers=headers, data=body)
        print(response)
        prediction = json.loads(response.content.decode('ascii'))
        print(prediction)
        os.remove(filename)
            # cd = form.cleaned_data
            # user = authenticate(
            #     request,
            #     username=cd['username'],
            #     password=cd['password'])
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
            #         return render(request, 'profile.html')
            #     else:
            #         return HttpResponse('Disabled account')
            # else:
        return HttpResponse(prediction)
        #myfile = request.FILES['myfile']
        
        #return HttpResponse('done')

    else:
    #     form = UploadImage()
         return render(request, 'upload.html')

# def uploadfile(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                 request,
#                 username=cd['username'],
#                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return render(request, 'profile.html')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid Login')
#     else:
#         form = UploadImage()
#         return render(request, 'login.html', {'form': form})
