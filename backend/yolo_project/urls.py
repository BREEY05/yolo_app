from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/", include("core.urls")),
    # Serve Vue frontend (catch-all) - must be last
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
] 

# Add static file serving for development
if settings.DEBUG:
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'dist', 'assets'))
    # Also serve the main index.html for all other routes (SPA handling)
    urlpatterns += [
        re_path(r'^.*/$', TemplateView.as_view(template_name='index.html')),
    ]
