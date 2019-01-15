import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Message

def index(request, page_num=1):
    start = (page_num-1)*10
    latest_message_list = Message.objects.filter(is_checked=True).order_by('-send_time')[start:start+10]
    if page_num == 1:
        last_page = 1
    else:
        last_page = page_num - 1
    if len(latest_message_list) < 10:
        next_page = page_num
    else:
        next_page = page_num + 1
    context = {
        'latest_message_list': latest_message_list,
        'next_page': last_page,
        'last_page': next_page,
    }
    return render(request, 'board/index.html', context)

def manage(request, page_num=1):
    start = (page_num-1)*10
    need_to_check_list = Message.objects.order_by('-send_time')[start:start+10]
    if page_num == 1:
        last_page = 1
    else:
        last_page = page_num - 1
    if len(need_to_check_list) <= 10:
        next_page = page_num
    else:
        next_page = page_num + 1
    context = {
        'need_to_check_list': need_to_check_list,
        'next_page': next_page,
        'last_page': last_page,
        'current_page': page_num,
    }
    return render(request, 'board/manage.html', context)

def write_message(request):
    if request.method == 'POST':
        print('POST DICT', request.POST)
        new_message = Message()
        new_message.message_text = request.POST['text-box']
        new_message.wechat_id = request.POST['wechat-box']
        new_message.save()
        return HttpResponseRedirect(reverse('board:index'), (1,))
    else:
        return render(request, 'board/write_message.html')

def check_pass(request, message_id, page_num=1):
    message = get_object_or_404(Message, id=message_id)
    message.is_checked = True
    message.save()
    return HttpResponseRedirect(reverse('board:manage'), (page_num,))

def detail(request, message_id, page_num=1):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        message.response_text = request.POST['text-box']
        message.save()
        return HttpResponseRedirect(reverse('board:manage'), (page_num,))
    else:
        context = {
            'message': message,
            'current_page': page_num,
        }
        return render(request, 'board/detail.html', context)