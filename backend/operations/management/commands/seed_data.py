import random
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from operations.models import Booking, Customer, Mechanic
class Command(BaseCommand):
    help="Creates realistic demo operations data."
    def handle(self,*args,**options):
        if Booking.objects.exists(): self.stdout.write(self.style.WARNING("Data already exists; skipping.")); return
        r=random.Random(42); first=["Aarav","Vivaan","Aditya","Riya","Ananya","Diya","Kabir","Ishaan","Meera","Arjun"]; last=["Sharma","Patel","Khan","Reddy","Gupta","Singh","Nair","Das"]
        Customer.objects.bulk_create([Customer(name=f"{r.choice(first)} {r.choice(last)}",email=f"customer{i}@example.com",phone=f"+91 98{r.randint(10000000,99999999)}") for i in range(75)]); customers=list(Customer.objects.all())
        Mechanic.objects.bulk_create([Mechanic(name=f"{r.choice(first)} {r.choice(last)}",phone=f"+91 97{r.randint(10000000,99999999)}",status=r.choice(["Available","On job","Offline"]),jobs_completed=r.randint(12,210)) for _ in range(24)]); mechanics=list(Mechanic.objects.all())
        services=[("Periodic service",(1599,3999)),("Battery replacement",(2799,6999)),("Tyre service",(999,4599)),("Engine diagnostics",(1199,3499)),("Emergency repair",(1999,7999))]; vehicles=["Honda City","Hyundai Creta","Maruti Baleno","Tata Nexon","Kia Seltos","Mahindra XUV300"]; statuses=[("Completed",.52),("Pending",.16),("Assigned",.13),("Mechanic On The Way",.11),("Cancelled",.08)]; now=timezone.now(); rows=[]
        for i in range(600):
            service,price=r.choice(services); roll=r.random(); running=0
            for value,weight in statuses:
                running+=weight
                if roll<=running: status=value; break
            rows.append(Booking(reference=f"IM-{10001+i}",customer=r.choice(customers),mechanic=None if status=="Pending" else r.choice(mechanics),vehicle=f"{r.choice(vehicles)} · {r.choice(['DL','MH','KA','TN'])}-{r.randint(10,99)}",service=service,status=status,amount=Decimal(r.randint(*price)),scheduled_at=now+timedelta(days=r.randint(-45,14),hours=r.randint(-10,10),minutes=r.choice([0,15,30,45]))))
        Booking.objects.bulk_create(rows); self.stdout.write(self.style.SUCCESS("Created 600 bookings, 75 customers and 24 mechanics."))
