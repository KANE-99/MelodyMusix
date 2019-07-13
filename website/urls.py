from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from music import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/',include('music.urls')),
    path('accounts/', include('django.contrib.auth.urls'),name='login'),
    path('accounts/signup/', views.signup, name="signup" )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
