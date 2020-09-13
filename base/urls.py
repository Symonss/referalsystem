from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/admin/',
         views.Admin_uSignUpView.as_view(), name='admin_signup'),
    path('accounts/signup/user/<str:code>',
         views.UserSignUpView.as_view(), name='user_signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
