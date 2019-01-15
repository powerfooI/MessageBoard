from django.shortcuts import render
from django.http import HttpResponse
from .models import Message


def index(request):
    latest_message_list = Message.objects.order_by('-send_time')[:5]
    context = {
        'latest_message_list': latest_message_list,
    }
    return render(request, 'board/index.html', context)

