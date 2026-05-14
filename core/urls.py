from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from orders import views   # ✅ FIXED — import your app views, not django.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("create-order/", views.create_order, name="create_order"),
    path("orders/", views.orders_list, name="orders"),   # ← COMMA ADDED
    path("logout/", auth_views.LogoutView.as_view(next_page='front_page'), name="logout"),
    path("notifications/", views.notifications, name="notifications"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


