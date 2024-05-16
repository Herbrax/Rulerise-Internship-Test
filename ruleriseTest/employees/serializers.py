from rest_framework import serializers
from .models import Employee, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        extra_kwargs = {
            'name': {'choices': Role.ROLE_CHOICES}
        }

class EmployeeSerializer(serializers.ModelSerializer):
    # 6. When fetching employee details, ensure that the job role is populated along with other employee information
    roles = RoleSerializer(many=True, read_only=True)
    role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), many=True, write_only=True, source='roles'
    )

    class Meta:
        model = Employee
        fields = '__all__'
