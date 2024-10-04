
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("core.urls")),
    path("ai/",include("smcg.urls")),
    path("ats/",include("ATS.urls")),
    path("cg/",include("CG.urls")),
    path("cp/",include("CP.urls")),
    path("feed360/",include("feed360.urls")),
    path("lin/",include("linkedin.urls")),
    path("rb/",include("resumebuilder.urls")),
    path("moci/",include("mockinterview.urls")),
    
    path('authentication/', include('authentication.urls')),
    path('utils/', include('utils.urls')),
    path("accounts/",include("django.contrib.auth.urls"))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)