"""URL mapping for the user API"""

from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('comments/', views.UserCommentViews
         .as_view({'get': 'list', 'post': 'create'}), name='Comment'),
    path('comments/<int:pk>', views.UserCommentViews
         .as_view({'delete': 'destroy'}), name='Delete comment with id'),
]
