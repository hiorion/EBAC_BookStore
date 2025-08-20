from django.contrib import admin
from django.urls import path, re_path, include
import debug_toolbar

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    re_path('bookstore/(?P<version>(v1|v2))/', include('product.urls')), 
    re_path('bookstore/(?P<version>(v1|v2))/', include('order.urls')), 
]
