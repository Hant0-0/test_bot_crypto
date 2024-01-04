
from django.contrib import admin
from django.urls import path


from admin_bot.views import UserAPI, UserStateDetailAPI, UserDetailAPI, UserStateAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', UserAPI.as_view()),
    path('api/user_detail/<int:user_id>/', UserDetailAPI.as_view()),
    path('api/users_state/', UserStateAPI.as_view()),
    path('api/user_state/<int:user_id>/', UserStateDetailAPI.as_view()),
]
