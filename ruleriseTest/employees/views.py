from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Employee, Role
from .serializers import EmployeeSerializer, RoleSerializer

'''
    1. Employee CRUD Operations: Create endpoints to perform CRUD operations on employee records.
    Ensure a well-structured payload for creating and updating employees.
    
    4.3 Provide an admin dashboard with endpoints to create and delete job roles.
    __________________
    
    ^ Done through ModelViewSet for basic CRUD operations 

    Get List of Employees : GET /api/employees/ 
    Create new Employee : POST /api/employees/ + Payload 
    Retrieve Employee : GET /api/employees/{id}/
    Update Employee : PUT /api/employees/{id}/ + Payload
    Patch Employee : PATCH /api/employees/{id}/ + Payload
    Delete Employee : DELETE /api/employees/{id}/

    Get List of Roles : GET /api/roles/ 
    Create new Role : POST /api/roles/ + Payload 
    Retrieve Role : GET /api/roles/{id}/
    Update Role : PUT /api/roles/{id}/ + Payload
    Patch Role : PATCH /api/roles/{id}/ + Payload
    Delete Role : DELETE /api/roles/{id}/
'''

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'id']
    filterset_fields = ['id']
    
    # 2.1 Role Assignment: Implement an endpoint to allow admins to assign roles to employees.
    # POST /api/employees/{id}/assign_roles/ + Payload
    @action(detail=True, methods=['post'])
    def assign_roles(self, request, pk=None):
        """
        Assign roles to an employee.
        Expects a list of role IDs in the request data.
        """
        employee = get_object_or_404(Employee, pk=pk)
        role_ids = request.data.get('role_ids', [])
        # Validate role IDs
        valid_role_ids = Role.objects.filter(id__in=role_ids).values_list('id', flat=True)
        invalid_role_ids = set(role_ids) - set(valid_role_ids)

        if invalid_role_ids:
            error_message = f"Invalid role IDs: {', '.join(map(str, invalid_role_ids))}"
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Assign roles to the employee
        roles = Role.objects.filter(id__in=valid_role_ids)
        employee.roles.set(roles)
        serializer = self.get_serializer(employee)
        return Response({'message': 'Roles assigned successfully', 'employee': serializer.data}, status=status.HTTP_200_OK)
    
    # 3. Search Functionality: Create endpoints to find employees by name and ID.
    # GET /api/employees/search/?q={search_term}
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search employees by first name, last name, or ID.
        Supports multiple search terms separated by spaces.
        Each term must match a word in the employee's first name, last name, or ID.
        """
        search_term = request.query_params.get('q', '')
        # Split the search term into individual terms
        terms = search_term.split()
        query = Q()
        # Build the query to match all terms
        for term in terms:
            # Each term must match a word in the first name, last name, or ID
            query &= (
                Q(first_name__icontains=term) | 
                Q(last_name__icontains=term) | 
                Q(id__icontains=term)
            )
        # Filter employees based on the query and ensure distinct results
        employees = self.get_queryset().filter(query).distinct()
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4.1. Admin Dashboard: Provide an admin dashboard with endpoints to retrieve total employees
    # GET /api/employees/total-employees/
    @action(detail=False, methods=['get'], url_path='total-employees')
    def total_employees(self, request):
        """
        Retrieve the total number of employees.
        """
        total = self.queryset.count()
        return Response({'total_employees': total}, status=status.HTTP_200_OK)

    # 5. Status Updates: Implement an endpoint allowing admins to update the status of an employee (employed or fired)
    # POST /api/employees/{id}/update-status/ + Payload
    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Update the status of an employee.
        Expects a boolean field "status" in the request data.
        """
        employee = get_object_or_404(Employee, pk=pk)
        status_value = request.data.get('status', True)
        employee.status = 'employed' if status_value else 'fired'
        employee.save()
        serializer = self.get_serializer(employee)
        status_message = 'employed' if status_value else 'fired'
        return Response({'message': f'Employee status updated to {status_message}', 'employee': serializer.data}, status=status.HTTP_200_OK)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['id']

    # 4.2. Admin Dashboard: Provide an admin dashboard with endpoints to retrieve total available roles.
    # GET /api/roles/total-roles/
    @action(detail=False, methods=['get'], url_path='total-roles')
    def total_roles(self, request):
        """
        Retrieve the total number of roles.
        """
        total = self.queryset.count()
        return Response({'total_roles': total}, status=status.HTTP_200_OK)