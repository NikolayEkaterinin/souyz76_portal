from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
]

handler404 = 'pages.views.page_not_found'

handler403 = 'pages.views.csrf_failure'

handler500 = 'pages.views.server_error'