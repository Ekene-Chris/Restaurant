from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('categories', views.CategoryList.as_view()),
    path('menu-items', views.MenuItemList.as_view()),
    path('cart/menu-items', views.CartList.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('groups/manager/users', views.ManagerView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view()),
    path('token/login/', obtain_auth_token, name='api_token_auth'),
    path('orders/<int:pk>/assign/', views.AssignOrderView.as_view()),
]