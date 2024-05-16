from django.urls import path, include
from rest_framework import routers
from employees.views import EmployeeViewSet, RoleViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    
    path('', include(router.urls)),
    path('api/', include('employees.urls')),
    

]