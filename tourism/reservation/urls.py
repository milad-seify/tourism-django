"""URL mappings for the reservation app"""


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reservation import views

router = DefaultRouter()
router.register('reservations', views.ReservationView)

app_name = 'reservation'  # for testing url in reverse in test file

urlpatterns = [
    path('', include(router.urls))
]
