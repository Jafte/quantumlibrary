from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/profile/$', views.UserProfile.as_view(), name="user_profile"),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^story/', include('story.urls')),

    url(r'^$', views.AppIndex.as_view(), name="home"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()