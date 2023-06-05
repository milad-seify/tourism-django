from django.urls import path, include
from rest_framework.routers import DefaultRouter
from place import views

router = DefaultRouter()
router.register(r'places', views.PlacesApiView, basename='places')
router.register(r'shopping', views.ShoppingApiView, basename='shipping')
router.register(r'tourism', views.TourismApiView, basename='tourism')
router.register(r'recreational', views.RecreationalApiView,
                basename='recreational')
app_name = 'place'


urlpatterns = [
    path('', include(router.urls))

]
