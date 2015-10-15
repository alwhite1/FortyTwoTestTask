from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'apps.person.views.main', name='main'),
    url(r'^requests/', 'apps.requests.views.requests', name='requests'),
    url(r'^edit/', 'apps.person.views.edit', name='edit'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'})

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)
