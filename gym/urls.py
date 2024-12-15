from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('main/', views.home, name='main'),
    path('membership/login/', views.membership_login, name='membership_login'),
    path('membership/signup/', views.membership_signup, name='membership_signup'),
    path('membership/dashboard/', views.membership_dashboard, name='membership_dashboard'),
    path('membership_dashboard_membership', views.membership_dashboard_membership, name='membership_dashboard_membership'),
    path('membership/dashboard/classes', views.membership_dashboard_classes, name='membership_dashboard_classes'),
    path('membership/logout/', views.membership_logout, name='membership_logout'),
    
    path('trainer/login/', views.trainer_login, name='trainer_login'),
    path('trainer/signup/', views.trainer_signup, name='trainer_signup'),
    path('trainer/dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/logout/', views.trainer_logout, name='trainer_logout'),
    
    path('classes/', views.gym_classes_list, name='gym_classes_list'),
    path('classes/add/', views.add_gym_class, name='add_gym_class'),
    path('classes/update/<str:class_id>/', views.update_gym_class, name='update_gym_class'),
    path('classes/delete/<str:class_id>/', views.delete_gym_class, name='delete_gym_class'),
    
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),
    path('equipment/update/<str:equipment_id>/', views.update_equipment, name='update_equipment'),
    path('equipment/delete/<str:equipment_id>/', views.delete_equipment, name='delete_equipment'),

    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('maintenance/update/<str:maintenance_id>/', views.update_maintenance, name='update_maintenance'),
    path('maintenance/delete/<str:maintenance_id>/', views.delete_maintenance, name='delete_maintenance'),
    
    path('promotions/', views.promotional_list, name='promotional_list'),
    path('promotions/add/', views.add_promotional, name='add_promotional'),
    path('promotions/update/<str:promotional_id>/', views.update_promotional, name='update_promotional'),
    path('promotions/delete/<str:promotional_id>/', views.delete_promotional, name='delete_promotional'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)