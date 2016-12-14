from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def index(request):
    # return HttpResponse('Hello Django!')
    return render(request,'index.html')

#登录
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')

		# if username == 'admin' and password == 'admin123':
		# 	#return HttpResponse('LOGIN SUCCESS!')
		# 	#return HttpResponseRedirect('/event_manage/')
			
		# 	response = HttpResponseRedirect('/event_manage/')
		# 	#response.set_cookie('user',username,3600) #添加浏览器cookie
			
		# 	request.session['user'] = username #将session信息记录到浏览器
		# 	return response
		# else:
		# 	return render(request, 'index.html',{'errors':'username or password error!'})

		#认证登录
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user) #登录
			request.session['user'] = username #将session信息记录到浏览器
			response = HttpResponseRedirect('/event_manage/')
			return response
		else:
			return render(request, 'index.html',{'errors':'username or password error!'})

#发布会管理
@login_required
def event_manage(request):
	#username = request.COOKIES.get('user','') #读取浏览器cookie
	event_list = Event.objects.all()
	username = request.session.get('user','')
	paginator = Paginator(event_list, 2)
	p = request.GET.get('page')
	try:
		events = paginator.page(p)
	except PageNotAnInteger:
		events = paginator.page(1)
	except EmptyPage:
		events = paginator.page(paginator.num_pages)
	return render(request, 'event_manage.html',{'user':username,'events':events})

#发布会名称搜索
@login_required
def search_name(request):
	username = request.session.get('user','')
	search_name = request.GET.get('name','')
	event_list = Event.objects.filter(name__contains=search_name)
	return render(request, 'event_manage.html',{'user':username,'events':event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
	#username = request.COOKIES.get('user','') #读取浏览器cookie
	guest_list = Guest.objects.all()
	username = request.session.get('user','')
	paginator = Paginator(guest_list, 2)
	p = request.GET.get('page')
	try:
		contacts = paginator.page(p)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)

	return render(request, 'guest_manage.html',{'user':username,'guests':contacts})

#签到页面
@login_required
def sign_index(request,event_id):
	event = get_object_or_404(Event,id=event_id)
	total = Guest.objects.filter(event=event_id)
	signed = Guest.objects.filter(event=event_id,sign='1')

	return render(request, 'sign_index.html',{'event':event,'total':total.count(),'signed':signed.count()})

#签到动作
@login_required
def sign_index_action(request,event_id):
	event = get_object_or_404(Event,id=event_id)
	phone = request.POST.get('phone','')
	
	total = Guest.objects.filter(event=event_id).count()
	signed = Guest.objects.filter(event=event_id,sign='1').count()
	result = Guest.objects.filter(phone=phone)
	if not result:
		return render(request, 'sign_index.html',{'event':event,'hit':'phone error.','total':total,'signed':signed})

	result = Guest.objects.filter(phone=phone,event_id=event_id)
	if not result:
		return render(request, 'sign_index.html',{'event':event,'hit':'event id or phone error.','total':total,'signed':signed})

	result = Guest.objects.get(phone=phone)
	if result.sign:
		return render(request, 'sign_index.html',{'event':event,'hit':'user has signed in.','total':total,'signed':signed})
	else:
		Guest.objects.filter(phone=phone).update(sign='1')
		signed = Guest.objects.filter(event=event_id,sign='1').count()
		return render(request, 'sign_index.html',{'event':event,"hit":"sign in SUCCESS!",'guest':result,'total':total,'signed':signed})

#退出登录
@login_required
def logout(request):
	auth.logout(request) #退出登录
	response = HttpResponseRedirect('/index')
	return response