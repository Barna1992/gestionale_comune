from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('issue/', include('issue.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='dashboard'), name='index'),
    path('accounts/', include('registration.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
