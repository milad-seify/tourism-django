"""URL mappings for the reservation app"""


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reservation import views

router = DefaultRouter()
router.register('reservations', views.ReservationView)
router.register(r'hotelandresidence', views.HotelAndResidenceView,
                basename='HotelAndResidence')
router.register(r'tourismtour', views.TourismTourView, 'TourismTour')
router.register(r'travelagency', views.TravelAgencyView,
                basename='TravelAgency')

# router.register('TouristTour', views.TouristTourView)
app_name = 'reservation'  # for testing url in reverse in test file

urlpatterns = [
    path('', include(router.urls)),
    # path('Hotel/', views.HotelAndResidenceView.as_view(), name="hotel"),


]
