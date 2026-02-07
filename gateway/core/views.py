from django.shortcuts import render
from django.http import JsonResponse

def health(request):
    print("sagar")
    return JsonResponse({
        "status":"running",
        "service name":"gateway"
    })

