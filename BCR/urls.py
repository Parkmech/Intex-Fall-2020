from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('applicant/', include('applicant.urls')),
    path('employer/', include('employer.urls')),
    path('login/', include('login.urls')),
    path('signup/',include('login.urls')),
    path('', include('login.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
