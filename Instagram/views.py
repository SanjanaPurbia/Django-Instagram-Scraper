from django.shortcuts import render
from django.http import HttpResponse
from time import sleep
from Scrapper.Scrapper import Instagram
# Create your views here.
def Scrapper(request):
    return render(request, "login.html")

def insta(username,password):
    return Instagram.scrap(username,password)

def server(request):

    if request.method =="POST":
        data = request.POST
        username = request.POST['username']
        password = request.POST['password']
        print(username,password,data)
        data = insta(username,password)
        if data == False:
            return render(request,'error.html')
        else:
            return render(request,'Instagram.html',data[0])
    else:
        return render(request,'error.html')



