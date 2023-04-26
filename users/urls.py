from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('update/', views.UserView.as_view(), name='user_update'),
    path('check/', views.AuthAPIView.as_view(), name='user_check'),
    path('login/', views.AuthAPIView.as_view(), name='user_login'),
    path('logout/', views.AuthAPIView.as_view(), name='logout_view'),
]
