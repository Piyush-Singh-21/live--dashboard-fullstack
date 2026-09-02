from django.urls import path
from . import views
urlpatterns=[path("dashboard/",views.dashboard),path("bookings/",views.bookings),path("bookings/export/",views.export_bookings),path("bookings/<int:booking_id>/",views.booking_detail),path("mechanics/",views.mechanics),path("customers/",views.customers)]
