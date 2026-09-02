from django.test import TestCase
from django.utils import timezone
from .models import Booking, Customer
class ApiTests(TestCase):
    def setUp(self):
        customer=Customer.objects.create(name="Test Customer",email="test@example.com",phone="123"); Booking.objects.create(reference="IM-TEST",customer=customer,vehicle="Test Car",service="Inspection",amount=1000,scheduled_at=timezone.now())
    def test_dashboard_has_metrics(self):
        response=self.client.get("/api/dashboard/"); self.assertEqual(response.status_code,200); self.assertEqual(response.json()["metrics"]["total_bookings"],1)
    def test_bookings_search(self):
        response=self.client.get("/api/bookings/?search=TEST"); self.assertEqual(response.status_code,200); self.assertEqual(response.json()["count"],1)
    def test_booking_status_can_be_updated(self):
        response=self.client.patch("/api/bookings/1/",data='{"status":"Assigned"}',content_type="application/json"); self.assertEqual(response.status_code,200); self.assertEqual(response.json()["status"],"Assigned")
