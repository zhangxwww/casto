from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from .models import User
import re


# Create your views here.
def index(request):
    if str(request.user) != 'AnonymousUser':
        return render(request, 'user/index.html', {'username': request.user})
    else:
        return render(request, 'user/index.html', {'username': u'用户'}) 


def signup(request):
    print(request)
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        print(username, password)
        if username == '' or password == '':
            return JsonResponse({'error': u'无效的用户名或密码', 'status': False})
        if not valid_password(password):
            return JsonResponse({'error': u'密码不合法，应包含字母和数字！', 'status': False})
        same_name = User.objects.filter(username=username)
        if len(same_name) > 0:
            return JsonResponse({'error': u'用户名已经被占用', 'status': False})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({'username': username, 'status': True})
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('../info/?type=alreadylogin')
        return render(request, 'user/signup.html', {})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == '' or password == '':
            return JsonResponse({'error': u'用户名和密码不能为空'})
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': u'未找到用户或密码错误'})
        django_login(request, user)
        return JsonResponse({'username': username, 'status': True})
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('../info/?type=alreadylogin')
        return render(request, 'user/login.html', {})


@login_required
def dashboard(request):
    if request.method == 'GET':
        return render(request, 'user/dashboard.html', {"username": request.user})


@login_required
def logout(request):
    django_logout(request)
    return redirect('../info/?type=logout')


def please_login(_):
    return JsonResponse({'error': 'please login'})


def valid_password(password):
    reg = r'^[A-Za-z0-9_]{6,18}$'
    if re.match(reg, password):
        has_number = False
        has_letter = False
        num_reg = '[0-9]'
        letter_reg = '[A-Za-z]'
        for c in password:
            if re.match(num_reg, c):
                has_number = True
            if re.match(letter_reg, c):
                has_letter = True
        return has_number and has_letter
    return False


def info(request):
    if request.method == 'GET':
        info_type = request.GET.get('type')
        if info_type == 'logout':
            resp_json = {
                'title': u'成功登出',
                'description': u'您已成功登出本站点，欢迎下次光临！',
                'addr': '../index/',
                'addr_desc': u'首页'
            }
            return render(request, 'user/info.html', resp_json)
        if info_type == 'alreadylogin':
            resp_json = {
                'title': u'已经登录',
                'description': u'您已登录本站点，请访问用户管理面板或选择登出本站点',
                'addr': '../dashboard/',
                'addr_desc': u'管理面板'
            }
            return render(request, 'user/info.html', resp_json)
