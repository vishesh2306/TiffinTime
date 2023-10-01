from django.shortcuts import render

def index(request):
    return render(request, '../tiffin/templates/index.html')
