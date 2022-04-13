from django.contrib import admin
from django.urls import (
    path,
    include,
    re_path,
)
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Courses API',
        default_version='v1',
        description='APIs for CourseApp',
        contact=openapi.Contact(email='nhan@gmail.com'),
        license=openapi.License(name='Nhan@2022')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('courses.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-swagger'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='swagger-redoc'),
]
