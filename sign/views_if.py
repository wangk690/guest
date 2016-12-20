from django.http import JsonResponse
from sign.models import Event
from django.core.exceptions import ValidationError

#添加发布会接口
def add_event(requset):
	eid = requset.POST.get('eid','') #发布会id
	name = requset.POST.get('name','') #发布会标题
	limit = requset.POST.get('limit','') #限制人数
	status = requset.POST.get('status','') #状态
	address = requset.POST.get('address','') #地址
	start_time = requset.POST.get('start_time','') #发布会时间

	if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
		return JsonResponse({'status':10021,'message':'parameter error'})

	result = Event.objects.filter(id = eid)
	if result:
		return JsonResponse({'status':10022,'message':'event id already exists'})

	result.Event.objects.filter(name = name)
	if result:
		return JsonResponse({'status':10023,'message':'event name already exists'})
 

	if status == '':
		status = 1

	try:
		Event.objects.create(id=eid,name=name,limit=limit,address=address,status=int(status),start_time=start_time)
	except ValidationError as e:
		error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.'
		return JsonResponse({'status':10024,'message':'error'})

	return JsonResponse({'status':200,'message':'add event success'})
