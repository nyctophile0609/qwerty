from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('not_meant_for_you/', admin.site.urls),
    path('api/',include('api.urls'))
]