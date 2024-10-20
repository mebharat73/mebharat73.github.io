from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("web.urls")),
    path('summernote/', include('django_summernote.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
 
    
]


# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


