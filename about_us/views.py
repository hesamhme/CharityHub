from django.shortcuts import HttpResponse
from django.shortcuts import render
from accounts.models import User


def about_us(request):
    objs = User.objects.all()
    context = {
        'records': objs
    }
    return render(request, 'about_us.html', context)

