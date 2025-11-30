
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
]
# from django.urls import path
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.urls import reverse

# @api_view(['GET'])
# def auth_root(request, format=None):
#         return Response({
#             'register': reverse('register', request=request, format=format),
#             'login': reverse('login', request=request, format=format),
#             'profile': reverse('profile', request=request, format=format),
#         })

# urlpatterns = [
#         path('', auth_root, name='auth-root'),
#         path('register/', views.register_user, name='register'),
#         path('login/', views.login_user, name='login'),
#         path('profile/', views.UserProfileView.as_view(), name='profile'),
#     ]