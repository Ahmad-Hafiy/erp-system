from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from hr import views as hr_views
from procurement import views as procurement_views

# Customize Admin portal headers and titles
admin.site.site_header = "Company ERP Administration"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "System Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', account_views.dashboard, name='dashboard'),

    # HR Endpoints
    path('hr/leave/apply/', hr_views.submit_leave, name='submit_leave'),
    path('hr/leave/<int:pk>/<str:action>/', hr_views.review_leave, name='review_leave'),
    path('hr/expense/apply/', hr_views.submit_expense, name='submit_expense'),
    path('hr/expense/<int:pk>/<str:action>/', hr_views.review_expense, name='review_expense'),

    # Procurement Endpoints
    path('procurement/apply/', procurement_views.submit_purchase, name='submit_purchase'),
    path('procurement/<int:pk>/<str:action>/', procurement_views.review_purchase, name='review_purchase'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)