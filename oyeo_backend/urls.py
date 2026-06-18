"""
URL configuration for oyeo_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contact/', include('contact.urls')),
    path('', TemplateView.as_view(template_name='Oyéo-services.html'), name='home'),
    path('Oyéo-services.html', TemplateView.as_view(template_name='Oyéo-services.html'), name='home_html'),
    path('page-services.html', TemplateView.as_view(template_name='page-services.html'), name='services'),
    path('page-tarif.html', TemplateView.as_view(template_name='page-tarif.html'), name='tarif'),
    path('Propos.html', TemplateView.as_view(template_name='Propos.html'), name='propos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # To serve the images directly from /images/ as referenced in the HTML:
    urlpatterns += static('/images/', document_root=settings.BASE_DIR / 'Template' / 'images')


