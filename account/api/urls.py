from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

app_name = 'account'

urlpatterns = [

	path('auth/', include('rest_framework.urls', namespace='rest_framework')),
	# path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

	# path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),

	# path("auth/", include("djoser.urls.base")),
	path("auth/", include("djoser.urls")),
    # path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
    # path("auth/", include("djoser.social.urls")),
]