from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Message


def index(request, page_num=1):
    total_pages = int((Message.objects.filter(is_checked=True).count() - 1) / 10 + 1)
    if page_num >= 99999:
        page_num = total_pages
    start = (page_num - 1) * 10
    latest_message_list = Message.objects.filter(is_checked=True).order_by('-send_time')[start:start + 10]
    if page_num == 1:
        last_page = 1
    else:
        last_page = page_num - 1
    if page_num == total_pages:
        next_page = page_num
    else:
        next_page = page_num + 1
    context = {
        'latest_message_list': latest_message_list,
        'next_page': next_page,
        'last_page': last_page,
        'current_page': page_num,
        'total_pages': total_pages
    }
    return render(request, 'board/index.html', context)


@login_required
def manage(request, page_num=1):
    start = (page_num - 1) * 10
    need_to_check_list = Message.objects.order_by('-send_time')[start:start + 10]
    total_pages = int((Message.objects.count() - 1) / 10 + 1)
    if page_num == 1:
        last_page = 1
    else:
        last_page = page_num - 1
    if page_num == total_pages:
        next_page = page_num
    else:
        next_page = page_num + 1
    context = {
        'need_to_check_list': need_to_check_list,
        'next_page': next_page,
        'last_page': last_page,
        'current_page': page_num,
        'total_pages': total_pages
    }
    return render(request, 'board/manage.html', context)


def write_message(request):
    if request.method == 'POST':
        new_message = Message()
        new_message.message_text = request.POST['text-box']
        new_message.wechat_id = request.POST['wechat-box']
        new_message.save()
        return HttpResponseRedirect(reverse('board:index'))
    else:
        return render(request, 'board/write_message.html')


@login_required
def check_pass(request, message_id, page_num=1):
    message = get_object_or_404(Message, id=message_id)
    message.is_checked = True
    message.save()
    return HttpResponseRedirect(reverse('board:manage'), (page_num,))


@login_required
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


def manager_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('board:manage'))
        else:
            return Http404()
    else:
        return render(request, 'board/login.html')


@login_required
def manager_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('board:index'))
