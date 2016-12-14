from django.test import TestCase
from sign.models import Guest,Event

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
		