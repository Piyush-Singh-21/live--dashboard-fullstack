import csv
import json
from datetime import timedelta
from django.db.models import Count, Sum, Q
from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from .models import Booking, Customer, Mechanic

def serialize(booking):
    return {"id":booking.id,"reference":booking.reference,"customer":booking.customer.name,"vehicle":booking.vehicle,"service":booking.service,"mechanic":booking.mechanic.name if booking.mechanic else None,"status":booking.status,"amount":float(booking.amount),"scheduled_at":booking.scheduled_at.isoformat()}
def dashboard(request):
    base=Booking.objects.select_related("customer","mechanic"); today=timezone.localdate()
    c=base.aggregate(total=Count("id"),completed=Count("id",filter=Q(status="Completed")),pending=Count("id",filter=Q(status="Pending")),cancelled=Count("id",filter=Q(status="Cancelled")),revenue=Sum("amount",filter=Q(status="Completed")))
    trend=[]
    for n in range(6,-1,-1):
        date=today-timedelta(days=n); x=base.filter(scheduled_at__date=date).aggregate(bookings=Count("id"),revenue=Sum("amount",filter=Q(status="Completed"))); trend.append({"label":date.strftime("%a"),"bookings":x["bookings"],"revenue":float(x["revenue"] or 0)})
    statuses=[{"name":x["status"],"value":x["value"]} for x in base.values("status").annotate(value=Count("id")).order_by("status")]
    services=[{"name":x["service"],"value":x["value"]} for x in base.values("service").annotate(value=Count("id")).order_by("-value")[:5]]
    return JsonResponse({"metrics":{"total_bookings":c["total"],"today_bookings":base.filter(scheduled_at__date=today).count(),"completed_bookings":c["completed"],"pending_bookings":c["pending"],"cancelled_bookings":c["cancelled"],"total_revenue":float(c["revenue"] or 0),"active_mechanics":Mechanic.objects.exclude(status="Offline").count(),"new_customers":Customer.objects.filter(created_at__date__gte=today-timedelta(days=30)).count()},"booking_trend":trend,"status_breakdown":statuses,"service_breakdown":services})
def bookings(request):
    items=Booking.objects.select_related("customer","mechanic"); term=request.GET.get("search","").strip(); status=request.GET.get("status")
    if term: items=items.filter(Q(reference__icontains=term)|Q(customer__name__icontains=term)|Q(vehicle__icontains=term))
    if status: items=items.filter(status=status)
    page=max(int(request.GET.get("page",1)),1); size=min(max(int(request.GET.get("page_size",20)),1),100); count=items.count(); start=(page-1)*size
    return JsonResponse({"count":count,"results":[serialize(x) for x in items[start:start+size]]})
def booking_detail(request,booking_id):
    try:
        booking=Booking.objects.select_related("customer","mechanic").get(pk=booking_id)
        if request.method == "PATCH":
            payload=json.loads(request.body or "{}")
            status=payload.get("status")
            if status not in Booking.Status.values: return JsonResponse({"detail":"Invalid booking status"},status=400)
            booking.status=status; booking.save(update_fields=["status"])
        return JsonResponse(serialize(booking))
    except Booking.DoesNotExist: raise Http404("Booking not found")
def mechanics(request):
    return JsonResponse({"results":[{"id":m.id,"name":m.name,"status":m.status,"jobs_completed":m.jobs_completed,"current_booking":next((x.reference for x in m.bookings.exclude(status__in=["Completed","Cancelled"])[:1]),None)} for m in Mechanic.objects.all()]})
def customers(request): return JsonResponse({"results":list(Customer.objects.values("id","name","email","phone","created_at"))})
def export_bookings(request):
    response=HttpResponse(content_type="text/csv"); response["Content-Disposition"]='attachment; filename="instant-mechanic-bookings.csv"'; writer=csv.writer(response); writer.writerow(["Booking ID","Customer","Vehicle","Service","Mechanic","Status","Amount","Scheduled"])
    for b in Booking.objects.select_related("customer","mechanic"): writer.writerow([b.reference,b.customer.name,b.vehicle,b.service,b.mechanic.name if b.mechanic else "",b.status,b.amount,b.scheduled_at.isoformat()])
    return response
