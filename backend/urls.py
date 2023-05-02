
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from accounts.views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('v1/api/',include('caro.api.urls')),
    path('v1/api/auth/',include('djoser.urls')),
    path('v1/api/auth/',include('djoser.urls.jwt')),
# path('v1/api/auth/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('v1/api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rooms/list/', list_rooms),
    path('rooms/create/', create_room),
    path('rooms/<int:room_id>/join/', join_room),
    path('rooms/<int:room_id>/quit/', quit_room),
    path('rooms/<int:room_id>/make_move/', make_move),
    path('rooms/<int:room_id>/update_board/', update_board),
    path('rooms/<int:room_id>/reset_room/', reset_room),
    path('rooms/<int:room_id>/delete_room/', delete_room),
]

# urlpatterns+= [re_path(r'^.*',TemplateView.as_view(template_name='index.html'))]
