from django.test import TestCase
from sign.models import Guest,Event
from django.test import Client
from django.contrib.auth.models import User
from datetime import datetime

# Create your tests here.
class ModelTest(TestCase):
	"""docstring for ModelTest"""
	
	def setUp(self):
		Event.objects.create(id=7,name='oneplus 4 event',status=True,limit=2000,address='shenzhen',start_time='2016-08-31 02:18:31')
		Guest.objects.create(id=7,event_id=7,realname='alena',phone='13712341235',email='alena@mail.com',sign=False)

	def test_event_model(self):
		result = Event.objects.get(name='oneplus 4 event')
		self.assertEqual(result.address, 'shenzhen')
		self.assertTrue(result.status)

	def test_guest_model(self):
		result = Guest.objects.get(phone='13712341235')
		self.assertEqual(result.realname, 'alena')
		self.assertFalse(result.sign)

class IndexPageTest(TestCase):
	'''测试index登录首页'''

	def test_index_page_render_index_template(self):
		'''测试index视图'''
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'index.html')
		
class LoginActionTest(TestCase):
	"""测试登录函数"""
	
	def setUp(self):
		User.objects.create_user('admin','admin@mail.com','admin123456')
		self.c = Client()

	def test_login_action_username_password_null(self):
		'''用户名密码为空'''
		test_data = {'username':'','password':''}
		response = self.c.post('/login_action/',data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'username or password error!', response.content)

	def test_login_action_username_password_error(self):
		'''用户名密码错误'''
		test_data = {'username':'abc','password':'123'}
		response = self.c.post('/login_action/',data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'username or password error!', response.content)

	def test_login_action_success(self):
		'''登录成功'''
		test_data = {'username':'admin','password':'admin123456'}
		response = self.c.post('/login_action/',data=test_data)
		self.assertEqual(response.status_code, 200)

class EventManageTest(TestCase):
	'''发布会管理'''
	def setUp(self):
		Event.objects.create(id=2,name='xiaomi5',limit=2000,status=True,address='beijing',start_time=datetime(2016,8,10,14,0,0))
		self.c = Client()

	def test_event_manage_success(self):
		'''测试发布会xiaomi5'''
		response = self.c.post('/event_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'xiaomi5', response.content)
		self.assertIn(b'beijing', response.content)

	def test_event_manage_search_success(self):
		'''测试发布会搜索'''
		response = self.c.post('/search_name/',{'name':'xiaomi5'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'xiaomi5', response.content)
		self.assertIn(b'beijing', response.content)
		
class GuestManageTest(TestCase):
	'''嘉宾管理'''
	def setUp(self):
		Event.objects.create(id=1,name='xiaomi5',limit=2000,status=True,address='beijing',start_time=datetime(2016,8,10,14,0,0))
		Guest.objects.create(event_id=1,realname='alena',phone='13712341235',email='alena@mail.com',sign=False)
		self.c=Client()

	def test_event_manage_success(self):
		'''测试嘉宾信息：alen'''
		response = self.c.post('/guest_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'alen', response.content)
		self.assertIn(b'13712341235', response.content)

	def test_guest_manage_serch_success(self):
		'''测试嘉宾搜索'''
		response = self.c.post('/search_phone/',{'phone':'13712341235'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'alen', response.content)
		self.assertIn(b'13712341235', response.content)

class SignIndexActionTest(TestCase):
	'''发布会签到'''
	def setUp(self):
		Event.objects.create(id=1,name='xiaomi5',limit=2000,status=True,address='beijing',start_time=datetime(2016,8,10,14,0,0))
		Event.objects.create(id=2,name='oneplus4',limit=2000,status=True,address='shenzhen',start_time=datetime(2016,5,6,14,0,0))
		Guest.objects.create(event_id=1,realname='alena',phone='13712341235',email='alena@mail.com',sign=False)
		Guest.objects.create(event_id=2,realname='una',phone='14100000001',email='una@mail.com',sign=True)

	def test_sign_index_action_phone_null(self)；
	'''手机号为空'''
