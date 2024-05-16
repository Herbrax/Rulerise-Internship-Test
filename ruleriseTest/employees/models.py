from django.db import models

class Role(models.Model):
    # 2.2 Valid roles: [manager, developer, design, scrum master].
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('scrum_master', 'Scrum Master'),
    ]
    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    # 5. Employee status can either be employed or fired
    STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('fired', 'Fired'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    hire_date = models.DateField()
    roles = models.ManyToManyField(Role, related_name='employees')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='employed')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
